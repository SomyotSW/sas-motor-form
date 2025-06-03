from flask import Flask, render_template, request, url_for
import os
from werkzeug.utils import secure_filename
from generate_pdf import generate_pdf
import smtplib
from email.message import EmailMessage

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = 'static/uploads'
os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)

SENDER_EMAIL = 'somyotsw442@gmail.com'
APP_PASSWORD = 'dfwj earf bvuj jcrv'
RECEIVER_EMAIL = 'somyot@synergy-as.com'

def send_email_with_pdf(subject, body, to_email, pdf_path):
    msg = EmailMessage()
    msg['Subject'] = subject
    msg['From'] = SENDER_EMAIL
    msg['To'] = to_email
    msg.set_content(body)

    with open(pdf_path, 'rb') as f:
        msg.add_attachment(f.read(), maintype='application', subtype='pdf', filename=os.path.basename(pdf_path))

    with smtplib.SMTP_SSL('smtp.gmail.com', 465) as smtp:
        smtp.login(SENDER_EMAIL, APP_PASSWORD)
        smtp.send_message(msg)

@app.route('/')
def form():
    return render_template('form.html')

@app.route('/submit', methods=['POST'])
def submit():
    requested_by = request.form['requested_by']
    motor_model = request.form['motor_model']
    motor_power = request.form['motor_power']
    power_unit = request.form['power_unit']
    gear_model = request.form['gear_model']
    gear_ratio = request.form['gear_ratio']
    voltage = request.form['voltage']
    customer_requirement = request.form['customer_requirement']
    accessories = request.form.getlist('accessory')

    motor_image = request.files['motor_image']
    gear_image = request.files['gear_image']
    installation_image = request.files['installation_image']

    def save_image(file):
        filename = secure_filename(file.filename)
        filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)
        file.save(filepath)
        return filepath

    motor_image_path = save_image(motor_image)
    gear_image_path = save_image(gear_image)
    installation_image_path = save_image(installation_image)

    pdf_filename = os.path.join(app.config['UPLOAD_FOLDER'], f"{motor_model}_report.pdf")
    generate_pdf(pdf_filename, {
        'requested_by': requested_by,
        'motor_model': motor_model,
        'motor_power': motor_power,
        'power_unit': power_unit,
        'gear_model': gear_model,
        'gear_ratio': gear_ratio,
        'voltage': voltage,
        'customer_requirement': customer_requirement,
        'accessories': accessories,
        'motor_image': motor_image_path,
        'gear_image': gear_image_path,
        'installation_image': installation_image_path
    })

    subject = "มีการลงทะเบียนมอเตอร์เกียร์ใหม่"
    body = f"Motor: {motor_model}\nGear: {gear_model}\nVoltage: {voltage}\nRequested by: {requested_by}"
    send_email_with_pdf(subject, body, RECEIVER_EMAIL, pdf_filename)

    return render_template('result.html',
                           motor_model=motor_model,
                           gear_model=gear_model,
                           voltage=voltage,
                           motor_image=motor_image_path,
                           gear_image=gear_image_path,
                           installation_image=installation_image_path,
                           pdf_file=os.path.basename(pdf_filename))

if __name__ == '__main__':
    app.run(debug=True)