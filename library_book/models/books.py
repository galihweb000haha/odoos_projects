from asyncio.log import logger
from odoo import models, fields
import logging

_logger = logging.getLogger(__name__)

class Books(models.Model):
    _name = 'books'

    library_id = fields.Many2one('library.book', string="Library")
    title = fields.Char(default="Title", string="Title")
    author = fields.Char(string="Author")
    language = fields.Char(string="Language")
    description = fields.Text(string="Description")
    genre = fields.Char(string="Genre")
    publisher = fields.Char(string="Publisher")
    published = fields.Date(string='Published', required=False,
        help='Initial publication')
    image_128 = fields.Image("Cover", max_width=128, max_height=128)


    def add_book(self):
        """
        this function will create new record in books table
        """
        _logger.warning("____create____")
        
        self.env['books'].create([
            {
                'title': '21 LESSONS',
                'author': 'Yuval Noah Harari',
                'language': 'English',
                'genre': 'Nonfiction',
                'publisher': 'Dvir Publishing House Ltd.'
            },
            {
                'title': 'Homo Deus',
                'author': 'Yuval Noah Harari',
                'language': 'English',
                'genre': 'Nonfiction',
                'publisher': 'Dvir Publishing House Ltd.'
            }
        ])

    def delete_book(self):
        """
        this function will delete a record in books table
        """
        _logger.warning("____delete____")

        # self.env['books'].search([('title', '=', 'percobaan')]).unlink()
        # self.env['books'].search([]).unlink()
        # _logger.warning("This>>>>>>>>>>>>>>>>>>>>>>>>>",self.env.ref('library_book.library_book_book_tree_view_id').read())
        _logger.warning("This>>>>>>>>>>>>>>>>>>>>>>>>>",self.env['books'].search([]).read())