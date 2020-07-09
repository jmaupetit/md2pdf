# From https://weasyprint.readthedocs.io/en/stable/tips-tricks.html
# Modified to accept CSS

from weasyprint import HTML, CSS


class PdfGenerator:
    """
    Generate a PDF out of a rendered template, with the possibility to integrate nicely
    a header and a footer if provided.

    Notes:
    ------
    - When Weasyprint renders an html into a PDF, it goes though several intermediate steps.
      Here, in this class, we deal mostly with a box representation: 1 `Document` have 1 `Page`
      or more, each `Page` 1 `Box` or more. Each box can contain other box. Hence the recursive
      method `get_element` for example.
      For more, see:
      https://weasyprint.readthedocs.io/en/stable/hacking.html#dive-into-the-source
      https://weasyprint.readthedocs.io/en/stable/hacking.html#formatting-structure
    - Warning: the logic of this class relies heavily on the internal Weasyprint API. This
      snippet was written at the time of the release 47, it might break in the future.
    - This generator draws its inspiration and, also a bit of its implementation, from this
      discussion in the library github issues: https://github.com/Kozea/WeasyPrint/issues/92
    """
    OVERLAY_LAYOUT = '@page {size: A4 portrait; margin: 0;}'

    def __init__(
        self,
        main_html,
        header_html=None,
        footer_html=None,
        base_url=None,
        stylesheets=[],
        side_margin=2,
        extra_vertical_margin=30
    ):
        """
        Parameters
        ----------
        main_html: str
            An HTML file (most of the time a template rendered into a string) which represents
            the core of the PDF to generate.
        header_html: str
            An optional header html.
        footer_html: str
            An optional footer html.
        base_url: str
            An absolute url to the page which serves as a reference to Weasyprint to fetch assets,
            required to get our media.
        side_margin: int, interpreted in cm, by default 2cm
            The margin to apply on the core of the rendered PDF (i.e. main_html).
        extra_vertical_margin: int, interpreted in pixel, by default 30 pixels
            An extra margin to apply between the main content and header and the footer.
            The goal is to avoid having the content of `main_html` touching the header or the
            footer.
        """
        self.main_html = main_html
        self.header_html = "<header>"+header_html+"</header>" if header_html else None
        self.footer_html = "<footer>"+footer_html+"</footer>" if footer_html else None
        self.base_url = base_url
        self.stylesheets = stylesheets
        self.side_margin = side_margin
        self.extra_vertical_margin = extra_vertical_margin

    def _compute_overlay_element(self, element: str):
        """
        Parameters
        ----------
        element: str
            Either 'header' or 'footer'

        Returns
        -------
        element_body: BlockBox
            A Weasyprint pre-rendered representation of an html element
        element_height: float
            The height of this element, which will be then translated in a html height
        """
        html = HTML(
            string=getattr(self, element+'_html'),
            base_url=self.base_url,
        )
        element_doc = html.render(stylesheets=[CSS(string=self.OVERLAY_LAYOUT), *self.stylesheets])
        element_page = element_doc.pages[0]
        element_body = PdfGenerator.get_element(element_page._page_box.all_children(), 'body')
        element_body = element_body.copy_with_children(element_body.all_children())
        element_html = PdfGenerator.get_element(element_page._page_box.all_children(), element)

        if element == 'header':
            element_height = element_html.height
        if element == 'footer':
            element_height = element_page.height - element_html.position_y

        return element_body, element_height

    def _apply_overlay_on_main(self, main_doc, header_body=None, footer_body=None):
        """
        Insert the header and the footer in the main document.

        Parameters
        ----------
        main_doc: Document
            The top level representation for a PDF page in Weasyprint.
        header_body: BlockBox
            A representation for an html element in Weasyprint.
        footer_body: BlockBox
            A representation for an html element in Weasyprint.
        """
        for page in main_doc.pages:
            page_body = PdfGenerator.get_element(page._page_box.all_children(), 'body')

            if header_body:
                page_body.children += header_body.all_children()
            if footer_body:
                page_body.children += footer_body.all_children()

    def render_pdf(self):
        """
        Returns
        -------
        pdf: a bytes sequence
            The rendered PDF.
        """
        if self.header_html:
            header_body, header_height = self._compute_overlay_element('header')
        else:
            header_body, header_height = None, 0
        if self.footer_html:
            footer_body, footer_height = self._compute_overlay_element('footer')
        else:
            footer_body, footer_height = None, 0

        margins = '{header_size}px {side_margin} {footer_size}px {side_margin}'.format(
            header_size=header_height + self.extra_vertical_margin,
            footer_size=footer_height + self.extra_vertical_margin,
            side_margin=str(self.side_margin)+'cm',
        )
        content_print_layout = '@page {size: A4 portrait; margin: %s;}' % margins

        html = HTML(
            string=self.main_html,
            base_url=self.base_url,
        )
        main_doc = html.render(stylesheets=[CSS(string=content_print_layout), *self.stylesheets])

        if self.header_html or self.footer_html:
            self._apply_overlay_on_main(main_doc, header_body, footer_body)
        pdf = main_doc.write_pdf()

        return pdf

    @staticmethod
    def get_element(boxes, element):
        """
        Given a set of boxes representing the elements of a PDF page in a DOM-like way, find the
        box which is named `element`.

        Look at the notes of the class for more details on Weasyprint insides.
        """
        for box in boxes:
            if box.element_tag == element:
                return box
            return PdfGenerator.get_element(box.all_children(), element)
