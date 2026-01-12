"""
搜索引擎
"""
import sys
from pathlib import Path
from typing import List, Dict, Tuple
import yaml

sys.path.insert(0, str(Path(__file__).parent.parent))

from storage.hbase_client import HBaseClient
from storage.data_model import Document
from search.tokenizer import Tokenizer
from search.ranking import TFIDF, BM25, calculate_title_weight


class Searcher:
    """
    搜索引擎
    """
    
    def __init__(self, hbase_client: HBaseClient = None):
        """
        初始化搜索引擎
        
        Args:
            hbase_client: HBase客户端
        """
        self.hbase_client = hbase_client or HBaseClient()
        self.tokenizer = Tokenizer()
        
        # 加载配置
        config_path = Path(__file__).parent.parent / 'config' / 'config.yaml'
        with open(config_path, 'r', encoding='utf-8') as f:
            config = yaml.safe_load(f)
        
        search_config = config.get('search', {})
        self.ranking_algorithm = search_config.get('ranking_algorithm', 'bm25')
        self.max_results = search_config.get('max_results', 50)
        
        # 加载索引数据
        self.documents: Dict[str, Document] = {}
        self.doc_tokens: Dict[str, List[str]] = {}
        self.inverted_index: Dict[str, Dict[str, int]] = {}
        
        self._load_index()
    
    def _load_index(self):
        """
        从HBase加载索引数据
        """
        print("Loading index from storage...")
        
        # 加载所有文档
        all_docs = self.hbase_client.get_all_documents()
        for doc in all_docs:
            doc_id = self._generate_doc_id(doc.url)
            self.documents[doc_id] = doc
        
        # 加载倒排索引
        # 由于HBase的限制，我们需要重新构建索引或使用其他方式存储
        # 这里简化处理，在搜索时动态构建
        print(f"Loaded {len(self.documents)} documents")
    
    def _generate_doc_id(self, url: str) -> str:
        """
        生成文档ID
        """
        import hashlib
        return hashlib.md5(url.encode()).hexdigest()
    
    def _build_doc_tokens(self):
        """
        构建文档分词结果（如果还没有）
        """
        if not self.doc_tokens:
            print("Building document tokens...")
            for doc_id, doc in self.documents.items():
                title_tokens = self.tokenizer.tokenize_title(doc.title)
                content_tokens = self.tokenizer.tokenize_content(doc.content)
                self.doc_tokens[doc_id] = title_tokens + content_tokens
            print("Document tokens built")
    
    def search(self, query: str, max_results: int = None) -> List[Tuple[Document, float]]:
        """
        搜索文档
        
        Args:
            query: 查询字符串
            max_results: 最大结果数量
            
        Returns:
            (文档, 分数) 列表，按分数降序排列
        """
        if not query or not query.strip():
            return []
        
        max_results = max_results or self.max_results
        
        # 分词
        query_tokens = self.tokenizer.tokenize(query)
        if not query_tokens:
            return []
        
        # 构建文档分词结果
        self._build_doc_tokens()
        
        # 找到包含查询词的文档
        candidate_docs = set()
        for token in query_tokens:
            found = False
            # 从倒排索引查找（如果已加载）
            if token in self.inverted_index:
                candidate_docs.update(self.inverted_index[token].keys())
                found = True

            # 即使有倒排索引，也要检查复合词匹配
            # 遍历所有文档，检查是否包含查询词（作为子串）
            for doc_id, tokens in self.doc_tokens.items():
                doc = self.documents[doc_id]
                # 检查标题和内容是否包含查询词
                if (token in doc.title or token in doc.content or
                    any(token in doc_token for doc_token in tokens)):
                    candidate_docs.add(doc_id)
        
        if not candidate_docs:
            return []
        
        # 计算相关性分数
        scores = []
        
        # 准备文档数据用于排序算法
        doc_list = []
        for doc_id in candidate_docs:
            doc = self.documents[doc_id]
            tokens = self.doc_tokens[doc_id]
            doc_list.append({
                'doc_id': doc_id,
                'doc': doc,
                'tokens': tokens
            })
        
        # 使用TF-IDF或BM25计算分数
        if self.ranking_algorithm == 'bm25':
            ranker = BM25(doc_list)
            for item in doc_list:
                doc_id = item['doc_id']
                doc = item['doc']
                tokens = item['tokens']
                
                # 计算BM25分数
                score = ranker.calculate_bm25(tokens, query_tokens)
                
                # 标题权重
                title_tokens = self.tokenizer.tokenize_title(doc.title)
                title_weight = calculate_title_weight(title_tokens, query_tokens)
                score *= title_weight
                
                scores.append((doc, score))
        else:
            # 使用TF-IDF
            ranker = TFIDF(doc_list)
            for item in doc_list:
                doc_id = item['doc_id']
                doc = item['doc']
                tokens = item['tokens']
                
                # 计算TF-IDF分数
                score = ranker.calculate_tfidf(tokens, query_tokens)
                
                # 标题权重
                title_tokens = self.tokenizer.tokenize_title(doc.title)
                title_weight = calculate_title_weight(title_tokens, query_tokens)
                score *= title_weight
                
                scores.append((doc, score))
        
        # 按分数排序
        scores.sort(key=lambda x: x[1], reverse=True)
        
        # 返回前max_results个结果
        return scores[:max_results]
    
    def search_by_source(self, query: str, source: str, max_results: int = None) -> List[Tuple[Document, float]]:
        """
        按来源搜索
        
        Args:
            query: 查询字符串
            source: 来源网站
            max_results: 最大结果数量
            
        Returns:
            (文档, 分数) 列表
        """
        results = self.search(query, max_results=None)
        filtered = [(doc, score) for doc, score in results if source in doc.source]
        max_results = max_results or self.max_results
        return filtered[:max_results]


