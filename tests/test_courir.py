import unittest
from craper.models.demandware import Courir

class TestCourirMethods(unittest.TestCase):
    def test_parse_pid(self):
        self.assertEqual(Courir.parse_pid(1488941), 1488941)
        self.assertEqual(Courir.parse_pid('1488941'), 1488941)
        self.assertEqual(Courir.parse_pid('01488941'), 1488941)
        self.assertEqual(Courir.parse_pid('001488941'), 1488941)

    def test_image_url(self):
        self.assertEqual(Courir.image_url(1488941), 'https://www.courir.com/on/demandware.static/-/Sites-master-catalog-courir/default/dw227c85ea/images/hi-res/001488941_101.png')
        self.assertEqual(Courir.image_url('1488941'), 'https://www.courir.com/on/demandware.static/-/Sites-master-catalog-courir/default/dw227c85ea/images/hi-res/001488941_101.png')
        self.assertEqual(Courir.image_url('01488941'), 'https://www.courir.com/on/demandware.static/-/Sites-master-catalog-courir/default/dw227c85ea/images/hi-res/001488941_101.png')
        self.assertEqual(Courir.image_url('001488941'), 'https://www.courir.com/on/demandware.static/-/Sites-master-catalog-courir/default/dw227c85ea/images/hi-res/001488941_101.png')
    
    def test_image_uri(self):
        self.assertEqual(Courir.image_uri(1488941), '/on/demandware.static/-/Sites-master-catalog-courir/default/dw227c85ea/images/hi-res/001488941_101.png')
        self.assertEqual(Courir.image_uri('1488941'), '/on/demandware.static/-/Sites-master-catalog-courir/default/dw227c85ea/images/hi-res/001488941_101.png')
        self.assertEqual(Courir.image_uri('01488941'), '/on/demandware.static/-/Sites-master-catalog-courir/default/dw227c85ea/images/hi-res/001488941_101.png')
        self.assertEqual(Courir.image_uri('001488941'), '/on/demandware.static/-/Sites-master-catalog-courir/default/dw227c85ea/images/hi-res/001488941_101.png')
    
    def test_format_pid(self):
        self.assertEqual(Courir.format_pid(1488941), '1488941')
        self.assertEqual(Courir.format_pid('1488941'), '1488941')
        self.assertEqual(Courir.format_pid('01488941'), '1488941')
        self.assertEqual(Courir.format_pid('001488941'), '1488941')
    
    def test_build_webhook(self):
        c = Courir()
        
        wh = c.build_webhook(int('FFADA2', 16), 'courir', '@rtunazzz', 1488941)
        self.assertEqual(wh, {
            'embeds': [
                {
                    "description": '```1488941```',
                    "color": 16756130,
                    "image": {
                        "url": 'https://www.courir.com/on/demandware.static/-/Sites-master-catalog-courir/default/dw227c85ea/images/hi-res/001488941_101.png',
                    },
                    "author": {
                        "name": 'courir',
                    },
                    "footer": {
                        "text": '@rtunazzz', 
                    },
                },
            ]
        })

if __name__ == '__main__':
    unittest.main()
