import os
from flask import Flask, render_template, request, redirect, url_for, flash
from models import Storage, Dealer , Product
from extensions import db
from flask_migrate import Migrate

app = Flask(__name__, template_folder='templates/')

# Database setup
basedir = os.path.abspath(os.path.dirname(__file__))
db_path = os.path.join(basedir, 'instance', 'inventory.db')

# Ensure the instance folder exists
os.makedirs(os.path.join(basedir, 'instance'), exist_ok=True)

app.config['SQLALCHEMY_DATABASE_URI'] = f"sqlite:///{db_path}"
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.secret_key = '9f8c2a4e3b9d1f2e5a6c7b8d9e0f1a2b'  # required for flash messages

# Initialize db with app
db.init_app(app)
migrate = Migrate(app, db)


@app.route('/')
def index():
    return "Inventory Management System Home Page"


# Dealers Routes

@app.route('/dealers')
def list_dealers():
    search_query = request.args.get('q', '').strip()
    if search_query:
        dealers = Dealer.query.filter(Dealer.name.ilike(f'%{search_query}%')).all()
    else:
        dealers = Dealer.query.all()
    return render_template('dealers.html', dealers=dealers)

@app.route('/dealer/add', methods=['GET', 'POST'])
def add_dealer():
    if request.method == 'POST':
        new_dealer = Dealer(
            name=request.form['name'],
            address=request.form.get('address'),
            state=request.form.get('state'),
            country=request.form.get('country'),
            pincode=request.form.get('pincode'),
            telephone=request.form.get('telephone'),
            mobile=request.form.get('mobile'),
            email=request.form.get('email'),
            gst_no=request.form.get('gst_no'),
            bank_name=request.form.get('bank_name'),
            account_no=request.form.get('account_no'),
            ifsc_code=request.form.get('ifsc_code')
        )
        db.session.add(new_dealer)
        db.session.commit()
        flash('Dealer added successfully.')
        return redirect(url_for('list_dealers'))
    return render_template('add_dealer.html')

# Edit Dealer Route
@app.route('/dealer/edit/<int:id>', methods=['GET', 'POST'])
def edit_dealer(id):
    dealer = Dealer.query.get_or_404(id)
    if request.method == 'POST':
        dealer.name = request.form['name']
        dealer.address = request.form.get('address')
        dealer.state = request.form.get('state')
        dealer.country = request.form.get('country')
        dealer.pincode = request.form.get('pincode')
        dealer.telephone = request.form.get('telephone')
        dealer.mobile = request.form.get('mobile')
        dealer.email = request.form.get('email')
        dealer.gst_no = request.form.get('gst_no')
        dealer.bank_name = request.form.get('bank_name')
        dealer.account_no = request.form.get('account_no')
        dealer.ifsc_code = request.form.get('ifsc_code')
        db.session.commit()
        flash('Dealer updated successfully.')
        return redirect(url_for('list_dealers'))
    return render_template('edit_dealer.html', dealer=dealer)

@app.route('/dealer/delete/<int:id>', methods=['POST'])
def delete_dealer(id):
    dealer = Dealer.query.get_or_404(id)
    db.session.delete(dealer)
    db.session.commit()
    flash('Dealer deleted successfully.')
    return redirect(url_for('list_dealers'))

# Storage Routes

@app.route('/storage')
def list_storage():
    q = request.args.get('q', '').strip()
    if q:
        storages = Storage.query.filter(
            Storage.base_name.ilike(f'%{q}%') |
            Storage.brand.ilike(f'%{q}%') |
            Storage.defined_name_with_spec.ilike(f'%{q}%')
        ).all()
    else:
        storages = Storage.query.all()
    return render_template('list_storage.html', storages=storages)



UNITS_LIST = ["Nos", "Kgs", "mm", "cm", "liters", "meters", "pieces", "packs"]

@app.route('/storage/add', methods=['GET', 'POST'])
def add_storage():
    dealers = Dealer.query.all()
    if request.method == 'POST':
        storage = Storage(
            base_name=request.form['base_name'],
            defined_name_with_spec=request.form['defined_name_with_spec'],
            brand=request.form['brand'],
            hsn_code=request.form['hsn_code'],
            dealer_id=request.form['dealer_id'],
            tax=request.form['tax'],
            current_stock=request.form['current_stock'],
            units=request.form['units'],
        )
        db.session.add(storage)
        db.session.commit()
        flash('Storage added successfully!')
        return redirect(url_for('list_storage'))
    return render_template('add_storage.html', dealers=dealers, units_list=UNITS_LIST)

@app.route('/storage/edit/<int:id>', methods=['GET', 'POST'])
def edit_storage(id):
    storage = Storage.query.get_or_404(id)
    dealers = Dealer.query.all()
    if request.method == 'POST':
        storage.base_name = request.form['base_name']
        storage.defined_name_with_spec = request.form['defined_name_with_spec']
        storage.brand = request.form['brand']
        storage.hsn_code = request.form['hsn_code']
        storage.dealer_id = request.form['dealer_id']
        storage.tax = request.form['tax']
        storage.current_stock = request.form['current_stock']
        storage.units = request.form['units']
        db.session.commit()
        flash('Storage updated!')
        return redirect(url_for('list_storage'))
    return render_template('edit_storage.html', storage=storage, dealers=dealers, units_list=UNITS_LIST)

@app.route('/storage/delete/<int:id>', methods=['POST'])
def delete_storage(id):
    storage = Storage.query.get_or_404(id)
    db.session.delete(storage)
    db.session.commit()
    flash('Storage deleted.')
    return redirect(url_for('list_storage'))


# Product Routes

@app.route('/product')
def list_product():
    products = Product.query.all()
    return render_template('list_product.html', products=products)

@app.route('/product/add', methods=['GET', 'POST'])
def add_product():
    storages = Storage.query.all()
    if request.method == 'POST':
        raw_material_ids = request.form.getlist('raw_materials')
        raw_materials = Storage.query.filter(Storage.id.in_(raw_material_ids)).all()
        new_product = Product(
            product_name=request.form['product_name'],
            product_description=request.form.get('product_description'),
            section_name=request.form.get('section_name'),
            qty=request.form.get('qty'),
            stock=request.form.get('stock'),
            raw_materials_used=raw_materials
        )
        db.session.add(new_product)
        db.session.commit()
        flash("Product added successfully")
        return redirect(url_for('list_product'))
    return render_template('add_product.html', storages=storages)

@app.route('/product/edit/<int:id>', methods=['GET', 'POST'])
def edit_product(id):
    product = Product.query.get_or_404(id)
    storages = Storage.query.all()
    if request.method == 'POST':
        product.product_name = request.form['product_name']
        product.product_description = request.form.get('product_description')
        product.section_name = request.form.get('section_name')
        product.qty = request.form.get('qty')
        product.stock = request.form.get('stock')
        raw_material_ids = request.form.getlist('raw_materials')
        product.raw_materials_used = Storage.query.filter(Storage.id.in_(raw_material_ids)).all()
        db.session.commit()
        flash("Product updated successfully")
        return redirect(url_for('list_product'))
    return render_template('edit_product.html', product=product, storages=storages)

@app.route('/product/delete/<int:id>', methods=['POST'])
def delete_product(id):
    product = Product.query.get_or_404(id)
    db.session.delete(product)
    db.session.commit()
    flash("Product deleted.")
    return redirect(url_for('list_product'))


if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    app.run(debug=True)
