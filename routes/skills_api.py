from flask import Blueprint, jsonify, request, session
from extensions import db
from models.skill import Skill
from sqlalchemy import or_

skills_api_bp = Blueprint('skills_api', __name__)

@skills_api_bp.route('/api/skills/search')
def search_skills():
    """Search skills by name or category"""
    query = request.args.get('q', '').strip()
    category = request.args.get('category', '').strip()
    limit = request.args.get('limit', 50, type=int)
    
    if not query and not category:
        return jsonify([])
    
    skill_query = Skill.query
    
    if query:
        skill_query = skill_query.filter(
            or_(
                Skill.skill_name.ilike(f'%{query}%'),
                Skill.description.ilike(f'%{query}%'),
                Skill.category.ilike(f'%{query}%')
            )
        )
    
    if category:
        skill_query = skill_query.filter(Skill.category.ilike(f'%{category}%'))
    
    skills = skill_query.order_by(Skill.skill_name).limit(limit).all()
    
    return jsonify([{
        'id': skill.id,
        'skill_name': skill.skill_name,
        'category': skill.category,
        'description': skill.description
    } for skill in skills])

@skills_api_bp.route('/api/skills/categories')
def get_categories():
    """Get all unique skill categories"""
    categories = db.session.query(Skill.category).distinct().filter(
        Skill.category.isnot(None)
    ).order_by(Skill.category).all()
    
    return jsonify([category[0] for category in categories])

@skills_api_bp.route('/api/skills/create', methods=['POST'])
def create_skill():
    """Create a new skill"""
    if 'user_id' not in session:
        return jsonify({'error': 'Authentication required'}), 401
    
    data = request.get_json()
    if not data:
        return jsonify({'error': 'No data provided'}), 400
    
    skill_name = data.get('skill_name', '').strip()
    category = data.get('category', '').strip()
    description = data.get('description', '').strip()
    
    if not skill_name:
        return jsonify({'error': 'Skill name is required'}), 400
    
    if not category:
        return jsonify({'error': 'Category is required'}), 400
    
    # Check if skill already exists
    existing_skill = Skill.query.filter_by(skill_name=skill_name).first()
    if existing_skill:
        return jsonify({'error': 'Skill already exists', 'skill': {
            'id': existing_skill.id,
            'skill_name': existing_skill.skill_name,
            'category': existing_skill.category,
            'description': existing_skill.description
        }}), 409
    
    try:
        # Create new skill
        new_skill = Skill(
            skill_name=skill_name,
            category=category,
            description=description
        )
        
        db.session.add(new_skill)
        db.session.commit()
        
        return jsonify({
            'success': True,
            'skill': {
                'id': new_skill.id,
                'skill_name': new_skill.skill_name,
                'category': new_skill.category,
                'description': new_skill.description
            },
            'message': f'Skill "{skill_name}" created successfully!'
        }), 201
        
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': f'Failed to create skill: {str(e)}'}), 500

@skills_api_bp.route('/api/skills/bulk')
def get_skills_bulk():
    """Get skills by multiple IDs"""
    skill_ids = request.args.getlist('ids')
    if not skill_ids:
        return jsonify([])
    
    try:
        skill_ids = [int(id) for id in skill_ids]
        skills = Skill.query.filter(Skill.id.in_(skill_ids)).all()
        
        return jsonify([{
            'id': skill.id,
            'skill_name': skill.skill_name,
            'category': skill.category,
            'description': skill.description
        } for skill in skills])
        
    except ValueError:
        return jsonify({'error': 'Invalid skill IDs'}), 400