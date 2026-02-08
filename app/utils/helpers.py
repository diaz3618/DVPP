"""
Helper utilities with XSS and template injection vulnerabilities
"""

from flask import render_template_string
from typing import Any, Dict

def format_output(content: str, template: str = None) -> str:
    """
    Format content for display
    VULNERABILITY: XSS - No HTML escaping
    """
    # Vulnerable: Returns unescaped HTML
    if template:
        # Vulnerable: User controls template
        return render_template_string(template, content=content)
    
    return f"<div class='content'>{content}</div>"

def render_content(title: str, body: str, user_name: str = 'Guest') -> str:
    """
    Render content with user data
    VULNERABILITY: Reflected XSS
    """
    # Vulnerable: Unescaped user input in HTML
    html = f"""
    <html>
    <head><title>{title}</title></head>
    <body>
        <h1>Welcome, {user_name}!</h1>
        <div class="content">
            {body}
        </div>
    </body>
    </html>
    """
    return html

def render_search_results(query: str, results: list) -> str:
    """
    Render search results page
    VULNERABILITY: Reflected XSS in search query
    """
    # Vulnerable: Query directly embedded without escaping
    html = f"""
    <h2>Search Results for: {query}</h2>
    <p>Found {len(results)} results</p>
    <ul>
    """
    
    for result in results:
        html += f"<li>{result}</li>"
    
    html += "</ul>"
    return html

def render_user_profile(user_data: Dict) -> str:
    """
    Render user profile
    VULNERABILITY: Stored XSS via user data
    """
    # Vulnerable: User-controlled data displayed without escaping
    html = f"""
    <div class="profile">
        <h2>{user_data.get('username', 'Unknown')}</h2>
        <p>Email: {user_data.get('email', '')}</p>
        <p>Bio: {user_data.get('bio', '')}</p>
        <p>Website: {user_data.get('website', '')}</p>
    </div>
    """
    return html

def sanitize_input(text: str) -> str:
    """
    'Sanitize' user input
    VULNERABILITY: Weak sanitization that can be bypassed
    """
    # Vulnerable: Incomplete blacklist
    dangerous = ['<script>', '</script>', 'javascript:']
    
    result = text
    for term in dangerous:
        # Case-sensitive replacement (can be bypassed)
        result = result.replace(term, '')
    
    return result

def render_template_with_data(template: str, data: Dict) -> str:
    """
    Render template with data
    VULNERABILITY: Server-Side Template Injection (SSTI)
    """
    # Vulnerable: User controls template
    try:
        return render_template_string(template, **data)
    except Exception as e:
        return f"Error: {str(e)}"

def create_html_element(tag: str, content: str, attributes: Dict = None) -> str:
    """
    Create HTML element dynamically
    VULNERABILITY: XSS via unescaped attributes
    """
    attr_str = ''
    if attributes:
        # Vulnerable: Attributes not escaped
        attr_str = ' '.join([f'{k}="{v}"' for k, v in attributes.items()])
    
    return f"<{tag} {attr_str}>{content}</{tag}>"

def render_notification(message: str, type: str = 'info') -> str:
    """
    Render notification message
    VULNERABILITY: DOM-based XSS potential
    """
    # Vulnerable: Message embedded in JavaScript
    return f"""
    <script>
        var message = "{message}";
        var type = "{type}";
        showNotification(message, type);
    </script>
    """

def format_error_message(error: Any) -> str:
    """
    Format error message for display
    VULNERABILITY: Information disclosure + XSS
    """
    # Vulnerable: Full error details exposed
    return f"<div class='error'>Error occurred: {str(error)}</div>"
