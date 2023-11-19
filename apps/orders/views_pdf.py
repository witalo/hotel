from reportlab.lib.colors import Color, black
from reportlab.lib.pagesizes import letter, landscape, A4, A5, C7
from reportlab.pdfgen import canvas

from .models import Order
from .number_letters import numero_a_moneda
import io
import pdfkit
import decimal
import reportlab
from django.contrib.auth.models import User
from django.http import HttpResponse
from reportlab.lib.pagesizes import landscape, A5, portrait, letter
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.platypus import SimpleDocTemplate, Paragraph, TableStyle, Spacer, Image, Flowable
from reportlab.platypus import Table
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.graphics.shapes import Drawing
from reportlab.graphics.barcode import qr
from reportlab.lib.enums import TA_CENTER, TA_LEFT, TA_JUSTIFY, TA_RIGHT
from reportlab.lib import colors
from reportlab.lib.units import cm, inch
from reportlab.rl_settings import defaultPageSize
from hotel import settings
import io
from django.conf import settings
import datetime
from datetime import datetime

from ..subsidiaries.models import Subsidiary

PAGE_HEIGHT = defaultPageSize[1]
PAGE_WIDTH = defaultPageSize[0]

styles = getSampleStyleSheet()
styles.add(ParagraphStyle(name='Right', alignment=TA_RIGHT, leading=8, fontName='Square', fontSize=8))
styles.add(ParagraphStyle(name='Justify', alignment=TA_JUSTIFY, leading=8, fontName='Square', fontSize=8))
styles.add(ParagraphStyle(name='Justify-Dotcirful', alignment=TA_JUSTIFY, leading=12, fontName='Dotcirful-Regular',
                          fontSize=10))
styles.add(
    ParagraphStyle(name='Justify-Dotcirful-table', alignment=TA_JUSTIFY, leading=12, fontName='Dotcirful-Regular',
                   fontSize=7))
styles.add(ParagraphStyle(name='Justify_Bold', alignment=TA_JUSTIFY, leading=8, fontName='Square-Bold', fontSize=8))
styles.add(ParagraphStyle(name='Center', alignment=TA_CENTER, leading=8, fontName='Square', fontSize=8))
styles.add(
    ParagraphStyle(name='Center-Dotcirful', alignment=TA_CENTER, leading=12, fontName='Dotcirful-Regular', fontSize=10))
styles.add(ParagraphStyle(name='Left', alignment=TA_LEFT, leading=8, fontName='Square', fontSize=8))
styles.add(ParagraphStyle(name='CenterTitle', alignment=TA_CENTER, leading=8, fontName='Square-Bold', fontSize=12))
styles.add(ParagraphStyle(name='CenterTitle-Dotcirful', alignment=TA_CENTER, leading=12, fontName='Dotcirful-Regular',
                          fontSize=10))
styles.add(ParagraphStyle(name='CenterTitle2', alignment=TA_CENTER, leading=8, fontName='Square-Bold', fontSize=12))
styles.add(ParagraphStyle(name='Center_Regular', alignment=TA_CENTER, leading=8, fontName='Ticketing', fontSize=10))
styles.add(ParagraphStyle(name='Center_Bold', alignment=TA_CENTER,
                          leading=8, fontName='Square-Bold', fontSize=12, spaceBefore=6, spaceAfter=6))
styles.add(ParagraphStyle(name='Center2', alignment=TA_CENTER, leading=8, fontName='Ticketing', fontSize=8))
styles.add(ParagraphStyle(name='Center3', alignment=TA_JUSTIFY, leading=8, fontName='Ticketing', fontSize=7))
style = styles["Normal"]

reportlab.rl_config.TTFSearchPath.append(str(settings.BASE_DIR) + '/static/admin/fonts')
pdfmetrics.registerFont(TTFont('Square', 'square-721-condensed-bt.ttf'))
pdfmetrics.registerFont(TTFont('Square-Bold', 'sqr721bc.ttf'))
pdfmetrics.registerFont(TTFont('Newgot', 'newgotbc.ttf'))
pdfmetrics.registerFont(TTFont('Ticketing', 'ticketing.regular.ttf'))
pdfmetrics.registerFont(TTFont('Lucida-Console', 'lucida-console.ttf'))
pdfmetrics.registerFont(TTFont('Square-Dot', 'square_dot_digital-7.ttf'))
pdfmetrics.registerFont(TTFont('Serif-Dot', 'serif_dot_digital-7.ttf'))
pdfmetrics.registerFont(TTFont('Enhanced-Dot-Digital', 'enhanced-dot-digital-7.regular.ttf'))
pdfmetrics.registerFont(TTFont('Merchant-Copy-Wide', 'MerchantCopyWide.ttf'))
pdfmetrics.registerFont(TTFont('Dot-Digital', 'dot_digital-7.ttf'))
pdfmetrics.registerFont(TTFont('Raleway-Dots-Regular', 'RalewayDotsRegular.ttf'))
pdfmetrics.registerFont(TTFont('Ordre-Depart', 'Ordre-de-Depart.ttf'))
pdfmetrics.registerFont(TTFont('Dotcirful-Regular', 'DotcirfulRegular.otf'))
pdfmetrics.registerFont(TTFont('Nationfd', 'Nationfd.ttf'))
pdfmetrics.registerFont(TTFont('Kg-Primary-Dots', 'KgPrimaryDots-Pl0E.ttf'))
pdfmetrics.registerFont(TTFont('Dot-line', 'Dotline-LA7g.ttf'))
pdfmetrics.registerFont(TTFont('Dot-line-Light', 'DotlineLight-XXeo.ttf'))
pdfmetrics.registerFont(TTFont('Jd-Lcd-Rounded', 'JdLcdRoundedRegular-vXwE.ttf'))

logo = "static/admin/images/logo.jpg"
watermark = "static/admin/images/logos.png"


def tickets(request, pk=None):
    _wt = 3.14 * inch - 8 * 0.05 * inch
    order_obj = Order.objects.get(pk=pk)
    client_obj = order_obj.client
    client_document = ""
    client_name = ""
    client_address = ""
    client_document = client_obj.document
    client_name = client_obj.names
    client_address = client_obj.address
    subsidiary_obj = None
    subsidiary_obj = order_obj.subsidiary

    _title = Paragraph(str(subsidiary_obj.name).replace("\n", "<br />"), styles["CenterTitle"])
    _title2 = Paragraph(str(subsidiary_obj.address).replace("\n", "<br />"), styles["CenterTitle"])
    _title3 = Paragraph('RUC: ' + str(subsidiary_obj.ruc).replace("\n", "<br />"), styles["CenterTitle"])

    date = order_obj.create_at
    _format_time = datetime.now().strftime('%H:%M:%S')
    _format_date = date.strftime("%d/%m/%Y")
    tbn_document = 'TICKET'
    line = '-------------------------------------------------------'

    I = Image(logo)
    I.drawHeight = 2.20 * inch / 2.9
    I.drawWidth = 3.4 * inch / 2.9

    _tbl_header = [
        [I, _title],
        ['', _title3],
        ['', _title2],
    ]

    header_page = Table(_tbl_header, colWidths=[_wt * 40 / 100, _wt * 60 / 100])
    style_table_header = [
        # ('GRID', (0, 0), (-1, -1), 0.9, colors.blue),  # all columns
        ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),  # all columns
        ('ALIGNMENT', (0, 0), (-1, -1), 'CENTER'),  # first column
        ('SPAN', (0, 0), (0, -1)),  # first row
        # ('BACKGROUND', (1, 2), (2, 2), colors.blue),  # SECOND column
        ('TOPPADDING', (0, 0), (-1, -1), 0),  # first column
        ('BOTTOMPADDING', (0, 0), (-1, -1), 5),
    ]
    header_page.setStyle(TableStyle(style_table_header))

    style_table = [
        ('FONTNAME', (0, 0), (-1, -1), 'Square'),  # all columns
        # ('GRID', (0, 0), (-1, -1), 0.5, colors.black),  # all columns
        ('FONTSIZE', (0, 0), (-1, -1), 8),  # all columns
        ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),  # all columns
        ('BOTTOMPADDING', (0, 0), (-1, -1), -2),  # all columns
        ('LEFTPADDING', (0, 0), (0, -1), 0.5),  # first column
        ('ALIGNMENT', (1, 0), (1, -1), 'LEFT'),  # second column
        ('RIGHTPADDING', (1, 0), (1, -1), 0.5),  # second column
    ]
    colwiths_table = [_wt * 30 / 100, _wt * 70 / 100]
    payment = '-'
    if order_obj.payments_set.exists():
        if order_obj.payments_set.first().account.type == 'E':
            payment = 'EFECTIVO'
        else:
            payment = 'DEPOSITO'

    if len(client_document) == 11:
        p0 = Paragraph(client_name.upper(), styles["Justify"])
        p1 = Paragraph(client_address.upper(), styles["Justify"])
        ana_c1 = Table(
            [('RUC ', client_document)] +
            [('RAZÓN SOCIAL: ', p0)] +
            [('DIRECCIÓN: ', p1)] +
            [('ATENDIDO POR: ', order_obj.user.username.upper() + " ")] +
            [('FECHA: ', _format_date + '  HORA: ' + _format_time)] +
            [('TIPO DE PAGO: ', payment)],
            colWidths=colwiths_table)
    elif len(client_document) != 11:
        p0 = Paragraph(client_name.upper(), styles["Left"])
        ana_c1 = Table(
            [('CLIENTE: N DOC ', client_document)] +
            [('SR(A): ', p0)] +
            [('ATENDIDO POR: ', order_obj.user.username.upper() + " ")] +
            [('FECHA: ', _format_date + '  HORA: ' + _format_time)] +
            [('TIPO DE PAGO:', payment)],
            colWidths=colwiths_table)

    ana_c1.setStyle(TableStyle(style_table))

    style_table = [
        ('FONTNAME', (0, 0), (-1, -1), 'Square'),  # all columns
        # ('GRID', (0, 0), (-1, -1), 0.5, colors.black),  # all columns
        ('FONTSIZE', (0, 0), (-1, -1), 8),  # all columns
        ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),  # all columns
        ('BOTTOMPADDING', (0, 0), (-1, -1), -2),  # all columns
        ('LEFTPADDING', (0, 0), (0, -1), 0.5),  # first column
        ('FONTNAME', (0, 0), (0, -1), 'Ticketing'),  # first column
        ('LEFTPADDING', (2, 0), (2, -1), 2),  # third column
        ('ALIGNMENT', (3, 0), (3, -1), 'RIGHT'),  # fourth column
        ('FONTSIZE', (3, 0), (3, -1), 12),  # fourth column
        ('FONTNAME', (3, 0), (3, -1), 'Ticketing'),  # fifth row [col 1:2]
        ('LEFTPADDING', (1, 0), (1, -1), 0.5),  # second column
        ('ALIGNMENT', (1, 0), (3, -1), 'RIGHT'),  # four column
        # ('BACKGROUND', (1, 0), (1, 0), colors.blue),  # four column
        ('SPAN', (1, 0), (3, 0)),  # first row
        ('SPAN', (0, 1), (1, 1)),  # second row
        ('SPAN', (2, 1), (3, 1)),  # second row
    ]
    p10 = Paragraph('SR(A): ' + client_document + ' - ' + client_name, styles["Justify"])
    colwiths_table = [_wt * 25 / 100, _wt * 25 / 100]
    ana_c2 = Table(
        [('CLIENTE:', p10, '', '')] +
        [('SEDE:', order_obj.id, 'FECHA:', str(_format_date))],
        colWidths=colwiths_table)
    ana_c2.setStyle(TableStyle(style_table))
    # -------
    my_style_table_detail = [
        ('FONTNAME', (0, 0), (-1, -1), 'Square'),
        # ('GRID', (0, 0), (-1, -1), 0.5, colors.black),
        ('FONTSIZE', (0, 0), (-1, -1), 8),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 1),
        ('LEFTPADDING', (0, 0), (0, -1), 0.5),  # first column
        ('ALIGNMENT', (1, 0), (1, -1), 'CENTER'),  # second column
        ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),  # first column
        ('ALIGNMENT', (2, 0), (2, -1), 'LEFT'),  # SECOND column
        ('ALIGNMENT', (3, 0), (4, -1), 'RIGHT'),  # third column
        ('ALIGNMENT', (0, 0), (0, -1), 'RIGHT'),  # four column
        ('RIGHTPADDING', (4, 0), (4, -1), 0.1),  # first column
        # ('BACKGROUND', (4, 0), (4, -1), colors.blue),  # four column
        ('RIGHTPADDING', (3, 0), (3, -1), 0.5),  # four column
    ]
    _rows = []
    sub_total = 0
    total = 0
    igv_total = 0
    _sum_total_multiply = 0
    room_product = str(order_obj.room.number) + ' : HABITACION'
    _rows.append((str(decimal.Decimal(1.00)), Paragraph(str(room_product), styles["Justify"]), str(order_obj.price),
                  str(order_obj.price)))
    for d in order_obj.orderdetail_set.all():
        if d.product:
            product = Paragraph(d.product.name, styles["Justify"])
        else:
            product = Paragraph(d.description.upper(), styles["Justify"])
        _rows.append((str(decimal.Decimal(round(d.quantity, 2))), product, str(d.price),
                      str(decimal.Decimal(round(d.quantity * d.price, 2)))))
        base_total = d.quantity * d.price
        base_amount = base_total / decimal.Decimal(1.1800)
        igv = base_total - base_amount
        sub_total = sub_total + base_amount
        total = total + base_total
        igv_total = igv_total + igv
        _sum_total_multiply += d.amount()
    ana_c_detail = Table(_rows,
                         colWidths=[_wt * 15 / 100, _wt * 40 / 100, _wt * 20 / 100, _wt * 25 / 100])
    ana_c_detail.setStyle(TableStyle(my_style_table_detail))

    my_style_table5 = [
        ('FONTNAME', (0, 0), (-1, -1), 'Square-Bold'),
        ('FONTSIZE', (0, 0), (-1, -1), 10),
        ('RIGHTPADDING', (3, 0), (-1, -1), 0),
        # ('BACKGROUND', (3, 0), (-1, -1), colors.blue),  # four column
        ('BOTTOMPADDING', (0, 0), (-1, -1), -3),
        ('LEFTPADDING', (0, 0), (-1, -1), 0),
        # ('GRID', (0, 0), (-1, -1), 0.5, colors.black),
        ('ALIGNMENT', (3, 0), (3, -1), 'RIGHT'),  # four column
    ]
    total = decimal.Decimal(_sum_total_multiply).quantize(decimal.Decimal('0.00'), rounding=decimal.ROUND_HALF_EVEN)
    base = round(total / decimal.Decimal(1.18), 2)
    igv = total - base
    ana_c8 = Table(
        # [('OP. NO GRAVADA', '', 'S/', str(base))] +
        # [('I.G.V.  (18.00)', '', 'S/', str(igv))] +
        [('TOTAL', '', 'S/.', str(total + order_obj.price))],
        colWidths=[_wt * 60 / 100, _wt * 10 / 100, _wt * 10 / 100, _wt * 20 / 100]
    )
    ana_c8.setStyle(TableStyle(my_style_table5))
    footer = 'SON: ' + numero_a_moneda(order_obj.total() + order_obj.price).upper()
    counter = order_obj.orderdetail_set.count()
    my_style_table6 = [
        # ('GRID', (0, 0), (-1, -1), 0.5, colors.blue),   # all columns
        ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),  # all columns
        ('ALIGNMENT', (0, 0), (0, -1), 'CENTER'),  # first column
        ('SPAN', (0, 0), (1, 0)),  # first row
    ]

    datatable = str(subsidiary_obj.ruc) + '/' + str(subsidiary_obj.business)
    ana_c9 = Table([(print_qr(datatable), '')], colWidths=[_wt * 99 / 100, _wt * 1 / 100])
    ana_c9.setStyle(TableStyle(my_style_table6))

    _dictionary = []
    _dictionary.append(header_page)
    # _dictionary.append(I)
    _dictionary.append(Spacer(-10, -10))
    # _dictionary.append(Paragraph(tbh_business_name.replace("\n", "<br />"), styles["Center_Bold_title"]))
    # _dictionary.append(Paragraph(tbh_business_address.replace("\n", "<br />"), styles["Center-text"]))
    _dictionary.append(Paragraph(line, styles["Center2"]))
    _dictionary.append(Spacer(0, -7))
    _dictionary.append(Paragraph(tbn_document, styles["Center_Bold"]))
    _dictionary.append(Spacer(-10, -3))
    _dictionary.append(Spacer(0, -5))
    _dictionary.append(
        Paragraph(str(order_obj.subsidiary.serial) + ' - ' + str(
            str(order_obj.number).zfill(10)),
                  styles["Center_Bold"]))
    _dictionary.append(Spacer(-5, -1))
    _dictionary.append(ana_c1)
    _dictionary.append(Paragraph(line, styles["Center2"]))
    _dictionary.append(Spacer(-1, -1))
    _dictionary.append(Paragraph('DETALLE DE PRODUCTOS', styles["Center_Regular"]))
    _dictionary.append(Spacer(-1, -1))
    _dictionary.append(Paragraph(line, styles["Center2"]))
    _dictionary.append(ana_c_detail)  # "ana_c2"
    _dictionary.append(Spacer(-1, -1))
    _dictionary.append(Paragraph(line, styles["Center2"]))
    _dictionary.append(Spacer(-2, -2))
    _dictionary.append(ana_c8)
    _dictionary.append(Paragraph(line, styles["Center2"]))
    _dictionary.append(Paragraph(footer, styles["Center"]))
    _dictionary.append(Spacer(-2, -2))
    _dictionary.append(Paragraph(line, styles["Center2"]))
    _dictionary.append(
        Paragraph("**COMPROBANTE INTERNO NO TRIBUTARIO**".replace('***', '"'), styles["Center2"]))
    _dictionary.append(Spacer(-10, -10))
    _dictionary.append(ana_c9)
    _dictionary.append(Spacer(-15, -15))
    _dictionary.append(Paragraph(line, styles["Center2"]))
    _dictionary.append(Spacer(-1, -1))
    _dictionary.append(Paragraph(
        "www.ivanet.com",
        styles["Center2"]))
    buff = io.BytesIO()

    ml = 0.09 * inch
    mr = 0.09 * inch
    ms = 0.09 * inch
    mi = 0.09 * inch

    doc = SimpleDocTemplate(buff,
                            pagesize=(3.14961 * inch, 5.5 * inch + (inch * 0.25 * counter)),
                            rightMargin=mr,
                            leftMargin=ml,
                            topMargin=ms,
                            bottomMargin=mi,
                            title=tbn_document
                            )
    doc.build(_dictionary)
    # doc.build(elements)
    # doc.build(Story)

    response = HttpResponse(content_type='application/pdf')
    # response['Content-Disposition'] = 'inline; filename="somefilename.pdf"'
    # response['Content-Disposition'] = 'attachment; filename="ORDEN[{}].pdf"'.format(
    #     str(order_obj.subsidiary_store.subsidiary.serial) + '-' + str(order_obj.id))

    response.write(buff.getvalue())
    buff.close()
    return response


def ticket(request, pk=None):
    _wt = 3.14 * inch - 8 * 0.05 * inch
    order_obj = Order.objects.get(pk=pk)
    client_obj = order_obj.client
    client_document = ""
    client_name = ""
    client_address = ""
    client_phone = ""
    if client_obj:
        client_document = client_obj.document
        client_name = client_obj.names
        client_address = client_obj.address
        client_phone = client_obj.phone
    subsidiary_obj = order_obj.subsidiary
    I = Image(logo)
    I.drawHeight = 2.20 * inch / 2.9
    I.drawWidth = 3.4 * inch / 2.9

    names = Paragraph(str(subsidiary_obj.name).replace("\n", "<br />"), styles["CenterTitle"])
    address = Paragraph(str(subsidiary_obj.address).replace("\n", "<br />"), styles["CenterTitle"])
    ruc = Paragraph('RUC: ' + str(subsidiary_obj.ruc).replace("\n", "<br />"), styles["CenterTitle"])

    tbl_header = [
        [I],
        [ruc],
        [names],
        [address]
    ]
    page_header = Table(tbl_header, colWidths=[_wt * 100 / 100])
    style_tbl_header = [
        # ('GRID', (0, 0), (-1, -1), 0.9, colors.blue),  # all columns
        ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),  # all columns
        ('ALIGNMENT', (0, 0), (-1, -1), 'CENTER'),  # all columns
        ('TOPPADDING', (0, 0), (-1, -1), -2),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 5),
    ]
    page_header.setStyle(TableStyle(style_tbl_header))
    line = '-------------------------------------------------------'
    init = order_obj.init
    init_date = '-'
    init_time = '-'
    if init:
        init_date = init.strftime("%d/%m/%Y")
        init_time = init.strftime('%H:%M:%S')
    end = order_obj.end
    end_date = '-'
    end_time = '-'
    if end:
        end_date = end.strftime("%d/%m/%Y")
        end_time = end.strftime('%H:%M:%S')

    refund = order_obj.date_refund
    refund_date = '-'
    refund_time = '-'
    if refund:
        refund_date = refund.strftime("%d/%m/%Y")
        refund_time = refund.strftime('%H:%M:%S')

    style_tbl_client = [
        ('FONTNAME', (0, 0), (-1, -1), 'Square'),  # all columns
        # ('GRID', (0, 0), (-1, -1), 0.5, colors.black),  # all columns
        ('FONTSIZE', (0, 0), (-1, -1), 8),  # all columns
        ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),  # all columns
        ('BOTTOMPADDING', (0, 0), (-1, -1), -2),  # all columns
        ('LEFTPADDING', (0, 0), (0, -1), 0.5),  # first column
        ('ALIGNMENT', (1, 0), (1, -1), 'LEFT'),  # second column
        ('RIGHTPADDING', (1, 0), (1, -1), 0.5),  # second column
    ]
    if len(client_document) == 11:
        page_client = Table(
            [('RUC ', client_document)] +
            [('RAZÓN SOCIAL: ', Paragraph(client_name.upper(), styles["Justify"]))] +
            [('DIRECCIÓN: ', Paragraph(client_address.upper(), styles["Justify"]))] +
            [('TELEFONO: ', Paragraph(client_phone, styles["Justify"]))] +
            [('ATENDIDO POR: ', order_obj.user.username.upper())] +
            [('FECHA INICIO: ', init_date + '  HORA: ' + init_time)] +
            [('FECHA TERMINO: ', end_date + '  HORA: ' + end_time)],
            colWidths=[_wt * 30 / 100, _wt * 70 / 100])
        page_client.setStyle(TableStyle(style_tbl_client))
    elif len(client_document) != 11:
        page_client = Table(
            [('Nº DOCUMENTO ', client_document)] +
            [('SR(A): ', Paragraph(client_name.upper(), styles["Left"]))] +
            [('ATENDIDO POR: ', order_obj.user.username.upper())] +
            [('FECHA INICIO: ', init_date + '  HORA: ' + init_time)] +
            [('FECHA TERMINO: ', end_date + '  HORA: ' + end_time)],
            colWidths=[_wt * 30 / 100, _wt * 70 / 100])
        page_client.setStyle(TableStyle(style_tbl_client))
    # ---------------------------------------DETALLE---------------------------------------------
    style_tbl_detail = [
        ('FONTNAME', (0, 0), (-1, -1), 'Square'),
        # ('GRID', (0, 0), (-1, -1), 0.5, colors.black),
        ('FONTSIZE', (0, 0), (-1, -1), 8),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 1),
        ('LEFTPADDING', (0, 0), (-1, -1), 0.5),  # first column
        ('ALIGNMENT', (1, 0), (1, -1), 'CENTER'),  # second column
        ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),  # first column
        ('ALIGNMENT', (2, 0), (2, -1), 'LEFT'),  # SECOND column
        ('ALIGNMENT', (2, 0), (3, -1), 'RIGHT'),  # third column
        ('ALIGNMENT', (0, 0), (0, -1), 'RIGHT'),  # third column
        ('RIGHTPADDING', (0, 0), (-1, -1), 0.8),  # first column
        ('BOTTOMPADDING', (1, 0), (1, -1), 5),
        # ('BACKGROUND', (4, 0), (4, -1), colors.blue),  # four column
        # ('RIGHTPADDING', (3, 0), (3, -1), 0.5),  # four column
    ]
    room_obj = order_obj.room
    rows = []
    total = round(decimal.Decimal(0.00), 2)
    counter = 0
    room_product = 'SERVICIO DE HABITACION Nº ' + str(order_obj.room.number)
    rows.append((str(round(decimal.Decimal(1.00), 2)), Paragraph(str(room_product), styles["Justify"]),
                 str(round(decimal.Decimal(order_obj.price), 2)),
                 str(round(decimal.Decimal(order_obj.price), 2))))
    total = total + round(decimal.Decimal(order_obj.price), 2)
    for d in order_obj.orderdetail_set.all():
        if d.product:
            product = Paragraph(str(d.product.name), styles["Justify"])
        else:
            product = Paragraph(str(d.description).upper(), styles["Justify"])
        rows.append((str(decimal.Decimal(round(d.quantity, 2))), product, str(round(decimal.Decimal(d.price), 2)),
                     str(round(decimal.Decimal(d.quantity * d.price), 2))))
        amount = decimal.Decimal(d.quantity * d.price)
        total = total + amount
        counter = counter + 1

    page_detail = Table(rows, colWidths=[_wt * 10 / 100, _wt * 60 / 100, _wt * 15 / 100, _wt * 15 / 100])
    page_detail.setStyle(TableStyle(style_tbl_detail))

    style_tbl_total = [
        ('FONTNAME', (0, 0), (-1, -1), 'Square-Bold'),
        ('FONTSIZE', (0, 0), (-1, -1), 10),
        ('RIGHTPADDING', (3, 0), (-1, -1), 0),
        # ('BACKGROUND', (3, 0), (-1, -1), colors.blue),  # four column
        ('BOTTOMPADDING', (0, 0), (-1, -1), -3),
        ('LEFTPADDING', (0, 0), (-1, -1), 0),
        # ('GRID', (0, 0), (-1, -1), 0.5, colors.black),
        ('ALIGNMENT', (3, 0), (3, -1), 'RIGHT'),  # four column
    ]
    page_total = Table(
        [('TOTAL', '', 'S/.', str(total))],
        colWidths=[_wt * 60 / 100, _wt * 10 / 100, _wt * 10 / 100, _wt * 20 / 100]
    )
    page_total.setStyle(TableStyle(style_tbl_total))
    # ------------------------TOTAL EN LETRA--------------------------------------------
    page_total_letter = 'SON: ' + numero_a_moneda(total).upper()
    # ------------------------------------QR--------------------------------------------
    style_tbl_qr = [
        # ('GRID', (0, 0), (-1, -1), 0.5, colors.blue),   # all columns
        ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),  # all columns
        ('ALIGNMENT', (0, 0), (-1, -1), 'CENTER'),  # first column
        # ('SPAN', (0, 0), (1, 0)),  # first row
    ]
    qr = str(names) + ':' + str(ruc) + '/' + 'HABITACION Nº ' + str(room_obj.number) + '/' + str(
        client_name) + ':' + str(client_document)
    page_qr = Table([('', print_qr(qr), '')],
                    colWidths=[_wt * 5 / 100, _wt * 90 / 100, _wt * 5 / 100]
                    )
    page_qr.setStyle(TableStyle(style_tbl_qr))

    pdf = []
    pdf.append(page_header)
    pdf.append(Spacer(-10, -2))
    pdf.append(Paragraph(line, styles["Center2"]))
    pdf.append(Spacer(0, -7))
    pdf.append(Paragraph('TICKET', styles["Center_Bold"]))
    pdf.append(Spacer(-10, -7))
    pdf.append(Paragraph(str(subsidiary_obj.serial) + ' - ' + str(
        str(order_obj.number).zfill(10)),
                         styles["Center_Bold"]))
    pdf.append(Spacer(-5, -1))
    pdf.append(page_client)
    pdf.append(Paragraph(line, styles["Center2"]))
    pdf.append(Spacer(-1, -1))
    pdf.append(Paragraph('DESCRIPCION DEL DETALLE', styles["Center_Regular"]))
    pdf.append(Spacer(-1, -1))
    pdf.append(Paragraph(line, styles["Center2"]))
    pdf.append(page_detail)  # "ana_c2"
    pdf.append(Spacer(-1, -1))
    pdf.append(Paragraph(line, styles["Center2"]))
    pdf.append(Spacer(-2, -2))
    pdf.append(page_total)
    pdf.append(Paragraph(line, styles["Center2"]))
    pdf.append(Paragraph(page_total_letter, styles["Center"]))
    pdf.append(Spacer(-2, -2))
    pdf.append(Paragraph(line, styles["Center2"]))
    pdf.append(
        Paragraph("**COMPROBANTE INTERNO NO TRIBUTARIO**".replace('***', '"'), styles["Center2"]))
    pdf.append(Spacer(-10, -2))
    pdf.append(Paragraph(line, styles["Center2"]))
    pdf.append(page_qr)
    pdf.append(Spacer(-15, -5))
    pdf.append(Paragraph(line, styles["Center2"]))
    pdf.append(Spacer(-1, -1))
    pdf.append(Paragraph(
        "www.ivanet.com",
        styles["Center2"]))
    buff = io.BytesIO()

    ml = 0.09 * inch
    mr = 0.09 * inch
    ms = 0.09 * inch
    mi = 0.09 * inch

    doc = SimpleDocTemplate(buff,
                            pagesize=(3.14961 * inch, 6.3 * inch + (inch * 0.25 * counter)),
                            rightMargin=mr,
                            leftMargin=ml,
                            topMargin=ms,
                            bottomMargin=mi,
                            title=str(order_obj.number)
                            )
    doc.build(pdf)
    # doc.build(elements)
    # doc.build(Story)

    response = HttpResponse(content_type='application/pdf')
    # response['Content-Disposition'] = 'inline; filename="somefilename.pdf"'
    # response['Content-Disposition'] = 'attachment; filename="ORDEN[{}].pdf"'.format(
    #     str(order_obj.subsidiary_store.subsidiary.serial) + '-' + str(order_obj.id))

    response.write(buff.getvalue())
    buff.close()
    return response


def ticket_refund(request, pk=None):
    _wt = 3.14 * inch - 8 * 0.05 * inch
    order_obj = Order.objects.get(pk=pk)
    client_obj = order_obj.client
    client_document = ""
    client_name = ""
    client_address = ""
    client_phone = ""
    if client_obj:
        client_document = client_obj.document
        client_name = client_obj.names
        client_address = client_obj.address
        client_phone = client_obj.phone
    subsidiary_obj = order_obj.subsidiary
    I = Image(logo)
    I.drawHeight = 2.20 * inch / 2.9
    I.drawWidth = 3.4 * inch / 2.9

    names = Paragraph(str(subsidiary_obj.name).replace("\n", "<br />"), styles["CenterTitle"])
    address = Paragraph(str(subsidiary_obj.address).replace("\n", "<br />"), styles["CenterTitle"])
    ruc = Paragraph('RUC: ' + str(subsidiary_obj.ruc).replace("\n", "<br />"), styles["CenterTitle"])

    tbl_header = [
        [I],
        [ruc],
        [names],
        [address]
    ]
    page_header = Table(tbl_header, colWidths=[_wt * 100 / 100])
    style_tbl_header = [
        # ('GRID', (0, 0), (-1, -1), 0.9, colors.blue),  # all columns
        ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),  # all columns
        ('ALIGNMENT', (0, 0), (-1, -1), 'CENTER'),  # all columns
        ('TOPPADDING', (0, 0), (-1, -1), -2),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 5),
    ]
    page_header.setStyle(TableStyle(style_tbl_header))
    line = '-------------------------------------------------------'
    init = order_obj.init
    init_date = '-'
    init_time = '-'
    if init:
        init_date = init.strftime("%d/%m/%Y")
        init_time = init.strftime('%H:%M:%S')
    end = order_obj.end
    end_date = '-'
    end_time = '-'
    if end:
        end_date = end.strftime("%d/%m/%Y")
        end_time = end.strftime('%H:%M:%S')

    refund = order_obj.date_refund
    refund_date = '-'
    refund_time = '-'
    if refund:
        refund_date = refund.strftime("%d/%m/%Y")
        refund_time = refund.strftime('%H:%M:%S')

    style_tbl_client = [
        ('FONTNAME', (0, 0), (-1, -1), 'Square'),  # all columns
        # ('GRID', (0, 0), (-1, -1), 0.5, colors.black),  # all columns
        ('FONTSIZE', (0, 0), (-1, -1), 8),  # all columns
        ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),  # all columns
        ('BOTTOMPADDING', (0, 0), (-1, -1), -2),  # all columns
        ('LEFTPADDING', (0, 0), (0, -1), 0.5),  # first column
        ('ALIGNMENT', (1, 0), (1, -1), 'LEFT'),  # second column
        ('RIGHTPADDING', (1, 0), (1, -1), 0.5),  # second column
    ]
    if len(client_document) == 11:
        page_client = Table(
            [('RUC ', client_document)] +
            [('RAZÓN SOCIAL: ', Paragraph(client_name.upper(), styles["Justify"]))] +
            [('DIRECCIÓN: ', Paragraph(client_address.upper(), styles["Justify"]))] +
            [('TELEFONO: ', Paragraph(client_phone, styles["Justify"]))] +
            [('ATENDIDO POR: ', order_obj.user.username.upper())] +
            [('FECHA INICIO: ', init_date + '  HORA: ' + init_time)] +
            [('FECHA TERMINO: ', end_date + '  HORA: ' + end_time)] +
            [('FECHA REINTEGRO: ', refund_date + '  HORA: ' + refund_time)],
            colWidths=[_wt * 30 / 100, _wt * 70 / 100])
        page_client.setStyle(TableStyle(style_tbl_client))
    elif len(client_document) != 11:
        page_client = Table(
            [('Nº DOCUMENTO ', client_document)] +
            [('SR(A): ', Paragraph(client_name.upper(), styles["Left"]))] +
            [('ATENDIDO POR: ', order_obj.user.username.upper())] +
            [('FECHA INICIO: ', init_date + '  HORA: ' + init_time)] +
            [('FECHA TERMINO: ', end_date + '  HORA: ' + end_time)] +
            [('FECHA REINTEGRO: ', refund_date + '  HORA: ' + refund_time)],
            colWidths=[_wt * 30 / 100, _wt * 70 / 100])
        page_client.setStyle(TableStyle(style_tbl_client))
    # ---------------------------------------DETALLE---------------------------------------------
    style_tbl_detail = [
        ('FONTNAME', (0, 0), (-1, -1), 'Square'),
        # ('GRID', (0, 0), (-1, -1), 0.5, colors.black),
        ('FONTSIZE', (0, 0), (-1, -1), 8),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 1),
        ('LEFTPADDING', (0, 0), (-1, -1), 0.5),  # first column
        ('ALIGNMENT', (1, 0), (1, -1), 'CENTER'),  # second column
        ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),  # first column
        ('ALIGNMENT', (2, 0), (2, -1), 'LEFT'),  # SECOND column
        ('ALIGNMENT', (2, 0), (3, -1), 'RIGHT'),  # third column
        ('ALIGNMENT', (0, 0), (0, -1), 'RIGHT'),  # third column
        ('RIGHTPADDING', (0, 0), (-1, -1), 0.8),  # first column
        ('BOTTOMPADDING', (1, 0), (1, -1), 5),
        # ('BACKGROUND', (4, 0), (4, -1), colors.blue),  # four column
        # ('RIGHTPADDING', (3, 0), (3, -1), 0.5),  # four column
    ]
    room_obj = order_obj.room
    rows = []
    total = round(decimal.Decimal(0.00), 2)
    if order_obj.refund:
        room_product = 'REINTEGRO HABITACION Nº ' + str(room_obj.number)
        rows.append(
            (str(round(decimal.Decimal(1.00), 2)), Paragraph(str(room_product), styles["Justify"]),
             str(round(decimal.Decimal(order_obj.refund), 2)),
             str(round(decimal.Decimal(order_obj.refund), 2))))
        page_detail = Table(rows, colWidths=[_wt * 10 / 100, _wt * 60 / 100, _wt * 15 / 100, _wt * 15 / 100])
        page_detail.setStyle(TableStyle(style_tbl_detail))
        total = round(decimal.Decimal(order_obj.refund), 2)
    else:
        room_product = 'SIN REINTEGRO DE HABITACION Nº ' + str(room_obj.number)
        rows.append(
            (str('-'), Paragraph(str(room_product), styles["Justify"]),
             str(round(decimal.Decimal(0.00), 2)),
             str(round(decimal.Decimal(0.00), 2))))
        page_detail = Table(rows, colWidths=[_wt * 10 / 100, _wt * 60 / 100, _wt * 15 / 100, _wt * 15 / 100])
        page_detail.setStyle(TableStyle(style_tbl_detail))

    style_tbl_total = [
        ('FONTNAME', (0, 0), (-1, -1), 'Square-Bold'),
        ('FONTSIZE', (0, 0), (-1, -1), 10),
        ('RIGHTPADDING', (3, 0), (-1, -1), 0),
        # ('BACKGROUND', (3, 0), (-1, -1), colors.blue),  # four column
        ('BOTTOMPADDING', (0, 0), (-1, -1), -3),
        ('LEFTPADDING', (0, 0), (-1, -1), 0),
        # ('GRID', (0, 0), (-1, -1), 0.5, colors.black),
        ('ALIGNMENT', (3, 0), (3, -1), 'RIGHT'),  # four column
    ]
    page_total = Table(
        [('TOTAL', '', 'S/.', str(total))],
        colWidths=[_wt * 60 / 100, _wt * 10 / 100, _wt * 10 / 100, _wt * 20 / 100]
    )
    page_total.setStyle(TableStyle(style_tbl_total))
    # ------------------------TOTAL EN LETRA--------------------------------------------
    page_total_letter = 'SON: ' + numero_a_moneda(total).upper()
    # ------------------------------------QR--------------------------------------------
    style_tbl_qr = [
        # ('GRID', (0, 0), (-1, -1), 0.5, colors.blue),   # all columns
        ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),  # all columns
        ('ALIGNMENT', (0, 0), (-1, -1), 'CENTER'),  # first column
        # ('SPAN', (0, 0), (1, 0)),  # first row
    ]
    qr = str(names) + ':' + str(ruc) + '/' + 'HABITACION Nº ' + str(room_obj.number) + '/' + str(
        client_name) + ':' + str(client_document)
    page_qr = Table([('', print_qr(qr), '')],
                    colWidths=[_wt * 5 / 100, _wt * 90 / 100, _wt * 5 / 100]
                    )
    page_qr.setStyle(TableStyle(style_tbl_qr))

    pdf = []
    pdf.append(page_header)
    pdf.append(Spacer(-10, -2))
    pdf.append(Paragraph(line, styles["Center2"]))
    pdf.append(Spacer(0, -7))
    pdf.append(Paragraph('TICKET DE REINTEGRO', styles["Center_Bold"]))
    pdf.append(Spacer(-10, -7))
    pdf.append(Paragraph(str(subsidiary_obj.serial) + ' - ' + str(
        str(order_obj.number).zfill(10)),
                         styles["Center_Bold"]))
    pdf.append(Spacer(-5, -1))
    pdf.append(page_client)
    pdf.append(Paragraph(line, styles["Center2"]))
    pdf.append(Spacer(-1, -1))
    pdf.append(Paragraph('DESCRIPCION', styles["Center_Regular"]))
    pdf.append(Spacer(-1, -1))
    pdf.append(Paragraph(line, styles["Center2"]))
    pdf.append(page_detail)  # "ana_c2"
    pdf.append(Spacer(-1, -1))
    pdf.append(Paragraph(line, styles["Center2"]))
    pdf.append(Spacer(-2, -2))
    pdf.append(page_total)
    pdf.append(Paragraph(line, styles["Center2"]))
    pdf.append(Paragraph(page_total_letter, styles["Center"]))
    pdf.append(Spacer(-2, -2))
    pdf.append(Paragraph(line, styles["Center2"]))
    pdf.append(
        Paragraph("**COMPROBANTE INTERNO NO TRIBUTARIO**".replace('***', '"'), styles["Center2"]))
    pdf.append(Spacer(-10, -2))
    pdf.append(Paragraph(line, styles["Center2"]))
    pdf.append(page_qr)
    pdf.append(Spacer(-15, -5))
    pdf.append(Paragraph(line, styles["Center2"]))
    pdf.append(Spacer(-1, -1))
    pdf.append(Paragraph(
        "www.ivanet.com",
        styles["Center2"]))
    buff = io.BytesIO()

    ml = 0.09 * inch
    mr = 0.09 * inch
    ms = 0.09 * inch
    mi = 0.09 * inch

    doc = SimpleDocTemplate(buff,
                            pagesize=(3.14961 * inch, 6.3 * inch),
                            rightMargin=mr,
                            leftMargin=ml,
                            topMargin=ms,
                            bottomMargin=mi,
                            title=str(order_obj.number)
                            )
    doc.build(pdf)
    # doc.build(elements)
    # doc.build(Story)

    response = HttpResponse(content_type='application/pdf')
    # response['Content-Disposition'] = 'inline; filename="somefilename.pdf"'
    # response['Content-Disposition'] = 'attachment; filename="ORDEN[{}].pdf"'.format(
    #     str(order_obj.subsidiary_store.subsidiary.serial) + '-' + str(order_obj.id))

    response.write(buff.getvalue())
    buff.close()
    return response


class DrawInvoice(Flowable):
    def _init_(self, width=200, height=3, count_row=None):
        self.width = width
        self.height = height
        self.count_row = count_row

    def wrap(self, *args):
        """Provee el tamaño del área de dibujo"""
        return (self.width, self.height)

    def draw(self):
        canvas = self.canv
        canvas.saveState()
        canvas.setLineWidth(4)
        canvas.setStrokeGray(0.9)
        canvas.setFillColor(Color(0, 0, 0, alpha=1))
        canvas.roundRect(-7, 1, 563, 90, 8, stroke=1, fill=0)
        canvas.restoreState()


def add_draw(canvas, doc):
    canvas.saveState()
    pageNumber = canvas._pageNumber
    if pageNumber > 0:
        canvas.setFillColor(Color(0, 0, 0, alpha=0.4))
        canvas.drawImage(watermark, 75, (doc.height - 370) / 2, width=400, height=400)
        canvas.setStrokeGray(0.3)
        # canvas.drawString(10 * cm, cm, 'Pagina ' + str(pageNumber))
        # p = Paragraph('Pagina ' + str(pageNumber),
        #               styles["narrow_center"])
        footer1 = Paragraph("CONDICIONES Y TÉRMINOS DEL SERVICIO",
                            styles["narrow_center_pie"])
        footer2 = Paragraph(
            "Los servicios deben ser ejecutados de acuerdo a las especificaciones técnicas indicadas en la Orden de Servicio o anexos a ella. Las facturas serán recepcionadas con una copia de la orden de servicio.",
            styles["narrow_center_pie"])
        footer3 = Paragraph("No se aceptarán facturas por montos diferentes a la presente orden de servicio.",
                            styles["narrow_center_pie"])
        # footer4 = Paragraph("NOTAS",
        #                     styles["narrow_center_pie"])
        footer5 = Paragraph("NOTA: La recepción de la presente orden de compra significa la aceptación de la misma.",
                            styles["narrow_center_pie"])
        w1, h1 = footer1.wrap(doc.width, doc.bottomMargin)
        w2, h2 = footer2.wrap(doc.width, doc.bottomMargin)
        w3, h3 = footer3.wrap(doc.width, doc.bottomMargin)
        # w4, h4 = footer4.wrap(doc.width, doc.bottomMargin)
        w5, h5 = footer5.wrap(doc.width, doc.bottomMargin)
        # w, h = p.wrap(doc.width, doc.bottomMargin)
        footer1.drawOn(canvas, doc.leftMargin, h1 + 35)
        footer2.drawOn(canvas, doc.leftMargin, h2 + 9)
        footer3.drawOn(canvas, doc.leftMargin, h3 + 9)
        # footer4.drawOn(canvas, doc.leftMargin, h4 + 9)
        footer5.drawOn(canvas, doc.leftMargin, h5)
        # p.drawOn(canvas, 10 * cm, h)
        canvas.setLineWidth(1)
        canvas.setStrokeColor(black)
        # canvas.line(15, 75, 580, 75)
        canvas.line(15, 52, 580, 52)
        # canvas.setFont('Times-Roman', 9)
        # canvas.setLineWidth(4)
        # canvas.setFillColor(Color(0, 0, 0, alpha=1))
        # canvas.setStrokeGray(0.9)
        # canvas.roundRect(18, 730, 563, 90, 8, stroke=1, fill=0)
        canvas.restoreState()


def print_qr(code):
    qr_code = qr.QrCodeWidget(code)
    bounds = qr_code.getBounds()
    width = bounds[2] - bounds[0]
    height = bounds[3] - bounds[1]
    drawing = Drawing(
        3.5 * cm, 3.5 * cm, transform=[3.5 * cm / width, 0, 0, 3.5 * cm / height, 0, 0])
    drawing.add(qr_code)
    return drawing


class NumberedCanvas(canvas.Canvas):
    def _init_(self, *args, **kwargs):
        canvas.Canvas._init_(self, *args, **kwargs)
        self._saved_page_states = []

    def showPage(self):
        self.saved_page_states.append(dict(self.__dict_))
        self._startPage()

    def save(self):
        """add page info to each page (page x of y)"""
        num_pages = len(self._saved_page_states)
        for state in self._saved_page_states:
            self._dict_.update(state)
            self.draw_page_number(num_pages)
            canvas.Canvas.showPage(self)
        canvas.Canvas.save(self)

    def draw_page_number(self, page_count):
        self.setFont("Narrow", 11)
        self.drawRightString(cm * 20.3, cm - 17,
                             "Pagina %d de %d" % (self._pageNumber, page_count))
