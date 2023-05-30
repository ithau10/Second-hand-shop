from django.contrib import admin
from django.http import HttpResponse
from django.urls import reverse
from django.utils.html import format_html
from .models import Banner,Category,Brand,Color,Size,Product,ProductAttribute,CartOrder,CartOrderItems,ProductReview,Wishlist,UserAddressBook
import io
from reportlab.pdfgen import canvas
# admin.site.register(Banner)
admin.site.register(Brand)
admin.site.register(Size)


class BannerAdmin(admin.ModelAdmin):
	list_display=('alt_text','image_tag')
admin.site.register(Banner,BannerAdmin)

class CategoryAdmin(admin.ModelAdmin):
    list_display = ('title', 'image_tag')
    search_fields = ['title']
    
admin.site.register(Category, CategoryAdmin)


class ColorAdmin(admin.ModelAdmin):
	list_display=('title','color_bg')
admin.site.register(Color,ColorAdmin)

from django.http import HttpResponse
from reportlab.lib import colors
from reportlab.lib.pagesizes import letter, landscape
from reportlab.lib.styles import getSampleStyleSheet
from reportlab.lib.units import inch
from reportlab.platypus import SimpleDocTemplate, Table, TableStyle

class ProductAdmin(admin.ModelAdmin):
    list_display = ('id', 'title', 'category', 'brand', 'stock', 'is_featured')
    list_editable = ('stock', 'is_featured')
    list_filter = ('title', 'category', 'brand', 'stock', 'is_featured')

    def generate_pdf_report(self, request, queryset):
        response = HttpResponse(content_type='application/pdf')
        response['Content-Disposition'] = 'attachment; filename="product_report.pdf"'

        # Create the PDF object, using the response object as its "file."
        doc = SimpleDocTemplate(response, pagesize=landscape(letter))
        styles = getSampleStyleSheet()

        # Create a list of lists containing the data for the table.
        data = [['Title', 'Category', 'Brand', 'Stock', 'Featured']]
        for product in queryset:
            data.append([product.id, product.title, product.category, product.brand, product.stock, product.is_featured])

        # Create the table object and set its style.
        table = Table(data)
        table.setStyle(TableStyle([
            ('BACKGROUND', (0, 0), (-1, 0), colors.grey),
            ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
            ('ALIGN', (0, 0), (-1, 0), 'CENTER'),
            ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
            ('FONTSIZE', (0, 0), (-1, 0), 14),
            ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
            ('BACKGROUND', (0, 1), (-1, -1), colors.beige),
            ('TEXTCOLOR', (0, 1), (-1, -1), colors.black),
            ('ALIGN', (0, 1), (-1, -1), 'CENTER'),
            ('FONTNAME', (0, 1), (-1, -1), 'Helvetica'),
            ('FONTSIZE', (0, 1), (-1, -1), 12),
            ('BOTTOMPADDING', (0, 1), (-1, -1), 6),
        ]))

        # Add the table to the PDF document and save it.
        doc.build([table])
        return response

    generate_pdf_report.short_description = 'Generate PDF report'

    actions = ['generate_pdf_report']

admin.site.register(Product, ProductAdmin)


# Product Attribute
class ProductAttributeAdmin(admin.ModelAdmin):
	list_display=('id','image_tag','product','price','color','size')
	list_filter = ('id','product','price','color','size')

admin.site.register(ProductAttribute,ProductAttributeAdmin)

# Order
from django.http import HttpResponse
from django.http import HttpResponse
from reportlab.lib import colors
from reportlab.lib.pagesizes import A4, inch
from reportlab.lib.styles import getSampleStyleSheet
from reportlab.lib.units import mm
from reportlab.platypus import SimpleDocTemplate, Table, TableStyle

class CartOrderAdmin(admin.ModelAdmin):
    list_editable=('paid_status','order_status')
    list_display=('user','total_amt','paid_status','order_dt','order_status')
    list_filter = ('order_dt','paid_status','order_status')
    actions = ['print_report']

    def print_report(self, request, queryset):
        # Create the HttpResponse object with the appropriate PDF headers.
        response = HttpResponse(content_type='application/pdf')
        response['Content-Disposition'] = 'attachment; filename="cart_order_report.pdf"'

        # Generate the PDF content and write it to the response.
        # Replace this code with your report generation logic.
        data = []
        for order in queryset:
            data.append([order.user, order.total_amt, order.paid_status, order.order_dt, order.order_status])

        # Create a table style
        table_style = TableStyle([
            ('BACKGROUND', (0,0), (-1,0), colors.grey),
            ('TEXTCOLOR',(0,0),(-1,0),colors.whitesmoke),
            ('ALIGN', (0,0), (-1,-1), 'CENTER'),
            ('FONTNAME', (0,0), (-1,0), 'Helvetica-Bold'),
            ('FONTSIZE', (0,0), (-1,0), 14),
            ('BOTTOMPADDING', (0,0), (-1,0), 12),
            ('BACKGROUND', (0,1), (-1,-1), colors.beige),
            ('TEXTCOLOR',(0,1),(-1,-1),colors.black),
            ('ALIGN', (0,1), (-1,-1), 'CENTER'),
            ('FONTNAME', (0,1), (-1,-1), 'Helvetica'),
            ('FONTSIZE', (0,1), (-1,-1), 12),
            ('BOTTOMPADDING', (0,1), (-1,-1), 6),
            ('GRID', (0,0), (-1,-1), 1, colors.black)
        ])

        # Create a table and set style
        table = Table(data)
        table.setStyle(table_style)

        # Create the PDF object, using the response object as its "file."
        buffer = io.BytesIO()
        doc = SimpleDocTemplate(buffer, pagesize=A4, rightMargin=30,leftMargin=30, topMargin=30,bottomMargin=18)
        elements = []

        # Add the table to the PDF object
        elements.append(table)
        doc.build(elements)

        # Get the value of the BytesIO buffer and write it to the response.
        pdf = buffer.getvalue()
        buffer.close()
        response.write(pdf)
        return response

    print_report.short_description = 'Print report'

admin.site.register(CartOrder, CartOrderAdmin)




class ProductReviewAdmin(admin.ModelAdmin):
	list_display=('user','product','review_text','get_review_rating')
	list_filter = ('user','product','review_text')
admin.site.register(ProductReview,ProductReviewAdmin)


admin.site.register(Wishlist)


from django.contrib import admin
from django.http import HttpResponse
from reportlab.lib.pagesizes import letter
from reportlab.lib import colors
from reportlab.lib.styles import getSampleStyleSheet
from reportlab.lib.units import inch
from reportlab.platypus import SimpleDocTemplate, Table, TableStyle

class UserAddressBookAdmin(admin.ModelAdmin):
    list_display = ('user','address','status')
    actions = ['generate_report']

    def generate_report(self, request, queryset):
        response = HttpResponse(content_type='application/pdf')
        response['Content-Disposition'] = 'attachment; filename="user_address_book_report.pdf"'
        doc = SimpleDocTemplate(response, pagesize=letter)
        styles = getSampleStyleSheet()
        data = []
        # Header row
        data.append(['User', 'Address', 'Status'])
        # Data rows
        for obj in queryset:
            data.append([obj.user.username, obj.address, obj.status])
        table = Table(data)
        table.setStyle(TableStyle([
            ('BACKGROUND', (0,0), (-1,0), colors.grey),
            ('TEXTCOLOR', (0,0), (-1,0), colors.whitesmoke),
            ('ALIGN', (0,0), (-1,-1), 'CENTER'),
            ('FONTNAME', (0,0), (-1,0), 'Helvetica-Bold'),
            ('FONTSIZE', (0,0), (-1,0), 14),
            ('BOTTOMPADDING', (0,0), (-1,0), 12),
            ('BACKGROUND', (0,1), (-1,-1), colors.beige),
            ('TEXTCOLOR', (0,1), (-1,-1), colors.black),
            ('FONTNAME', (0,1), (-1,-1), 'Helvetica'),
            ('FONTSIZE', (0,1), (-1,-1), 12),
            ('ALIGN', (0,1), (-1,-1), 'LEFT'),
            ('VALIGN', (0,0), (-1,-1), 'MIDDLE'),
            ('TEXTCOLOR', (0,-1), (-1,-1), colors.red),
            ('FONTNAME', (0,-1), (-1,-1), 'Helvetica-Bold'),
            ('FONTSIZE', (0,-1), (-1,-1), 12),
            ('TOPPADDING', (0,-1), (-1,-1), 12),
            ('BOTTOMPADDING', (0,-1), (-1,-1), 12),
        ]))
        doc.build([table])
        return response
    generate_report.short_description = "Generate report"

admin.site.register(UserAddressBook, UserAddressBookAdmin)
