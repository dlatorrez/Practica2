from flask import request, redirect, render_template, session, flash
from server import app
from db import get_data_connection, get_users_connection

@app.route('/admin/companies')
def admin_list_companies():
    if session.get('role') != 'admin':
        return render_template('errors/403.html'), 403
    conn = get_data_connection()
    companies = conn.execute("SELECT * FROM companies").fetchall()
    conn.close()
    return render_template('admin/admin_companies.html', companies=companies)

@app.route('/admin/companies/add', methods=['GET', 'POST'])
def admin_add_company():
    if session.get('role') != 'admin':
        return render_template('errors/403.html'), 403
    if request.method == 'POST':
        company_name = request.form['company_name']
        owner = request.form['owner']

        conn_u = get_users_connection()
        user = conn_u.execute("SELECT username FROM users WHERE username = ?", (owner,)).fetchone()
        conn_u.close()
        
        if not user:
            flash(f"Error: El usuario '{owner}' no existe en el sistema.", "danger")
            return redirect('/admin/companies')

        conn = get_data_connection()
        conn.execute("INSERT INTO companies (name, owner) VALUES (?, ?)", (company_name, owner))
        conn.commit()
        conn.close()
        flash("Company created successfully.", "success")
        return redirect('/admin/companies')
    return render_template('admin/admin_companies.html')

@app.route('/admin/companies/delete', methods=['POST'])
def delete_company():
    if session.get('role') != 'admin':
        return render_template('errors/403.html'), 403
    company = request.form['company']
    conn = get_data_connection()
    conn.execute("DELETE FROM companies WHERE id = ?", (company,))
    conn.execute("DELETE FROM comments WHERE company_id = ?", (company,))
    conn.commit()
    conn.close()
    flash("Company deleted.", "warning")
    return redirect('/admin/companies')
