import unittest
import os
from utils.markdown_parser import parse_markdown
from llama_index.core import Document

class TestMarkdownParser(unittest.TestCase):
    
    def setUp(self):
        # Sample markdown content similar to your actual files
        self.sample_markdown = """
        ---
        id: 19152
        title: เมิน ‘ปชป.’ พลิกร่วมรัฐบาล ‘ณัฐพงษ์’ ยัน ‘ปชน.’ ทำหน้าที่ฝ่ายค้านให้ดีที่สุด 
        slug: the-people's-party-insists-on-performing-its-full-opposition-duties-even-though-the-democrat-party-has-decided-to-join-the-government
        publishedAt: 2024-08-28 17:27:00
        locale: th
        excerpt: ‘หัวหน้าพรรคประชาชน’ ลั่นเราไม่ได้ยื่นมือไปหาเขา! หลัง ‘บิ๊กป้อม’ ถูกเทเตรียมตัวสู่ฝ่ายค้าน บอกคงทำอะไรไม่ได้ ทำได้แค่ทำดีที่สุด ปัดให้ความเห็น ‘ปชป.’ พลิกร่วมรัฐบาล ยันทำหน้าที่ฝ่ายค้านให้เต็มที่ 
        category: การเมือง, politics, การเมืองระดับชาติ, national
        tags: []
        ---
        
        ## Highlights
        - ‘หัวหน้าพรรคประชาชน’ ลั่นเราไม่ได้ยื่นมือไปหาเขา! หลัง ‘บิ๊กป้อม’ ถูกเทเตรียมตัวสู่ฝ่ายค้าน
        - บอกคงทำอะไรไม่ได้ ทำได้แค่ทำดีที่สุด ปัดให้ความเห็น ‘ปชป.’ พลิกร่วมรัฐบาล ยันทำหน้าที่ฝ่ายค้านให้เต็มที่ 

        ## Content

        รัฐสภา (28 สิงหาคม 2567) **ณัฐพงษ์ เรืองปัญญาวุฒิ** สส.บัญชีรายชื่อ หัวหน้าพรรคประชาชน (ปชน.) ให้สัมภาษณ์ถึงการจับมือกันระหว่างพรรคเพื่อไทย (พท.) และพรรคประชาธิปัตย์ (ปชป.) ว่า เป็นสิ่งที่ทั้ง 2 พรรคไปพูดคุยกัน เราคงไม่ไปแสดงความเห็น และขอทำหน้าที่แกนนำพรรคฝ่ายค้านให้เต็มที่ที่สุดก่อน
        """
        
        # Write this content to a temporary file
        self.test_file_path = "test_markdown.md"
        with open(self.test_file_path, 'w', encoding='utf-8') as f:
            f.write(self.sample_markdown)
    
    def tearDown(self):
        # Clean up: remove the temporary file
        os.remove(self.test_file_path)
    
    def test_parse_markdown(self):
        # Parse the markdown file
        documents = parse_markdown(self.test_file_path)
        
        # Print document metadata for debugging
        for doc in documents:
            print(doc.metadata)
        
        # Check if we have the right number of documents
        self.assertEqual(len(documents), 1)
        
        # Check the content of the first document
        doc = documents[0]
        self.assertIsInstance(doc, Document)
        self.assertEqual(doc.metadata['id'], '19152')
        self.assertEqual(doc.metadata['title'].strip(), "เมิน ‘ปชป.’ พลิกร่วมรัฐบาล ‘ณัฐพงษ์’ ยัน ‘ปชน.’ ทำหน้าที่ฝ่ายค้านให้ดีที่สุด".strip())
        self.assertIn("ณัฐพงษ์ เรืองปัญญาวุฒิ", doc.text)
    
if __name__ == '__main__':
    unittest.main()