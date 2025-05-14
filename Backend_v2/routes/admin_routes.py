"""
user_routes.py

This file contains the routes for user information.
"""
import logging
from quart import jsonify, request
from quart_jwt_extended import jwt_required

from services import UserService

from utils.settings import settings