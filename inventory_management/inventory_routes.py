from flask import Blueprint, request, jsonify
from extensions import db
from models import InventoryItem
from flask_login import login_required, current_user

inventory = Blueprint('inventory', __name__)

# Create a new inventory item
@inventory.route('/items', methods=['POST'])
@login_required
def create_item():
    data = request.get_json()
    new_item = InventoryItem(
        item_name=data['item_name'],
        description=data.get('description', ''),
        quantity=data['quantity'],
        price=data['price'],
        user_id=current_user.id
    )
    db.session.add(new_item)
    db.session.commit()
    return jsonify({'message': 'Item created successfully!'}), 201

# Read all items for the current user
@inventory.route('/items', methods=['GET'])
@login_required
def get_items():
    items = InventoryItem.query.filter_by(user_id=current_user.id).all()
    items_data = [
        {
            'id': item.id,
            'item_name': item.item_name,
            'description': item.description,
            'quantity': item.quantity,
            'price': item.price
        }
        for item in items
    ]
    return jsonify(items_data), 200

# Read a specific inventory item by ID
@inventory.route('/items/<int:item_id>', methods=['GET'])
@login_required
def get_item(item_id):
    item = InventoryItem.query.filter_by(id=item_id, user_id=current_user.id).first()
    if not item:
        return jsonify({'error': 'Item not found or access denied'}), 404

    item_data = {
        'id': item.id,
        'item_name': item.item_name,
        'description': item.description,
        'quantity': item.quantity,
        'price': item.price
    }
    return jsonify(item_data), 200

# Update an inventory item by ID
@inventory.route('/items/<int:item_id>', methods=['PUT'])
@login_required
def update_item(item_id):
    item = InventoryItem.query.filter_by(id=item_id, user_id=current_user.id).first()
    if not item:
        return jsonify({'error': 'Item not found or access denied'}), 404

    data = request.get_json()
    item.item_name = data.get('item_name', item.item_name)
    item.description = data.get('description', item.description)
    item.quantity = data.get('quantity', item.quantity)
    item.price = data.get('price', item.price)
    db.session.commit()
    return jsonify({'message': 'Item updated successfully!'}), 200

# Delete an inventory item by ID
@inventory.route('/items/<int:item_id>', methods=['DELETE'])
@login_required
def delete_item(item_id):
    item = InventoryItem.query.filter_by(id=item_id, user_id=current_user.id).first()
    if not item:
        return jsonify({'error': 'Item not found or access denied'}), 404

    db.session.delete(item)
    db.session.commit()
    return jsonify({'message': 'Item deleted successfully!'}), 200
