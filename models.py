from extensions import db
from sqlalchemy.orm import relationship

class Dealer(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(120), nullable=False)
    address = db.Column(db.String(250))
    state = db.Column(db.String(100))        # New
    country = db.Column(db.String(100))      # New
    pincode = db.Column(db.String(20))       # New
    telephone = db.Column(db.String(50))     # landline
    mobile = db.Column(db.String(50))
    email = db.Column(db.String(120))
    gst_no = db.Column(db.String(50))
    bank_name = db.Column(db.String(100))
    account_no = db.Column(db.String(100))
    ifsc_code = db.Column(db.String(50))
    materials = db.relationship('Storage', back_populates='dealer', lazy = 'dynamic')


# Association Table for Many-to-Many Product <-> Storage (raw materials used)
product_material = db.Table('product_material',
    db.Column('product_id', db.Integer, db.ForeignKey('product.id')),
    db.Column('storage_id', db.Integer, db.ForeignKey('storage.id'))
)

class Storage(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    base_name = db.Column(db.String(128))
    defined_name_with_spec = db.Column(db.String(256))
    brand = db.Column(db.String(128))
    hsn_code = db.Column(db.String(32))
    dealer_id = db.Column(db.Integer, db.ForeignKey('dealer.id'))  # Foreign key to Dealer
    dealer = db.relationship('Dealer', back_populates='materials')
    tax = db.Column(db.Float)
    current_stock = db.Column(db.Float)
    units = db.Column(db.String(32))
    # Many-to-many with Product
    products = db.relationship('Product', secondary=product_material, back_populates = 'raw_materials_used')


class Product(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    product_name = db.Column(db.String(128), nullable=False)
    product_description = db.Column(db.Text)
    section_name = db.Column(db.String(128))
    qty = db.Column(db.Integer)
    stock = db.Column(db.Integer)
    raw_materials_used = db.relationship('Storage', secondary=product_material, back_populates='products')
    
class BOM(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    product_id = db.Column(db.Integer, db.ForeignKey('product.id'))
    product_quantity = db.Column(db.Integer)
    consignee = db.Column(db.String(128))
    date = db.Column(db.Date)
    material_collected = db.Column(db.Boolean, default=False)
    product = db.relationship('Product')

class PurchaseOrder(db.Model):
    po_no = db.Column(db.Integer, primary_key=True)
    material_name = db.Column(db.String(128))
    brand = db.Column(db.String(128))
    dealer_id = db.Column(db.Integer, db.ForeignKey('dealer.id'))
    dealer = db.relationship('Dealer')
    qty = db.Column(db.Integer)
    price = db.Column(db.Float)
    discount = db.Column(db.Float)
    total = db.Column(db.Float)
    gst = db.Column(db.Float)
    grand_total = db.Column(db.Float)
    date = db.Column(db.Date)
    status = db.Column(db.String(20))  # sent, waiting, unsent

class MaterialInward(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    po_no = db.Column(db.Integer, db.ForeignKey('purchase_order.po_no'))
    po = db.relationship('PurchaseOrder')
    dealer_name = db.Column(db.String(128))
    po_date = db.Column(db.Date)
    date_of_inward = db.Column(db.Date)
    bill_no = db.Column(db.String(64))
    bill_date = db.Column(db.Date)
    cost = db.Column(db.Float)
    payment_method = db.Column(db.String(64))  # cash paid, bank transfer
    pending_materials = db.Column(db.Text)     # serialized list (can store json string)

class MaterialOutward(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    material_details = db.Column(db.String(256))
    receiver_section = db.Column(db.String(128))  # In-company section or Branch outward
    qty = db.Column(db.Integer)
    date = db.Column(db.Date)
    reason = db.Column(db.String(256))

class Section(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    section_name = db.Column(db.String(128))
    products_they_create = db.Column(db.Text)  # can store JSON or plain text
    inventory_details = db.Column(db.Text)     # can store JSON or plain text
    product_development_status = db.Column(db.String(256))
