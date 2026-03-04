<?php
/**
 * Application Configuration
 * 
 * BASE_URL: The subfolder path where this app is served.
 * - Local XAMPP (symlink):  '/ramzaan'
 * - Production (domain root): ''
 * 
 * API_BASE: The Django backend API URL.
 * - Local development:  'http://localhost:8000'
 * - Production:         'https://api.madrasjamaatportal.org'
 * 
 * Change ONLY these values when switching environments.
 */
define('BASE_URL', '/ramzaan');
define('API_BASE', 'http://localhost:8000');
