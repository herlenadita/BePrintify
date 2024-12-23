from flask import Flask, request, jsonify, send_file,render_template_string
import base64
import subprocess
import pdfkit
import os
import time
import json
from flask_cors import CORS

# Define options
optionsA4 = {
    'page-size': 'A4',
    'margin-top': '0.5in',
    'margin-right': '0.5in',
    'margin-bottom': '0.5in',
    'margin-left': '0.5in',
    'encoding': 'UTF-8',
    'no-outline': None
}

# Define options
optionsA5 = {
    'page-size': 'A5',
    'margin-top': '0.5in',
    'margin-right': '0.5in',
    'margin-bottom': '0.5in',
    'margin-left': '0.5in',
    'encoding': 'UTF-8',
    'no-outline': None
}


app = Flask(__name__)
CORS(app)

config = pdfkit.configuration(wkhtmltopdf='/usr/bin/wkhtmltopdf')

# A simple hardcoded username and password (for demonstration)
valid_username = "user123"
valid_password = "password123"

# Login endpoint
@app.route('/login', methods=['POST'])
def login():
    data = request.get_json()

    # Extract username and password from request
    username = data.get('username')
    password = data.get('password')
    
    
    param = f"(record {{ \"username\" = \"{username}\"; \"password\" = \"{password}\" }})"
    print(param)
    command = [
    'dfx', 
    'canister', 
    'call', 
    'login-app-backend', 
    'login',
    param
    ]

    # Run the command and capture the output
    result = subprocess.run(command, capture_output=True, text=True)

    # Print the output of the command
    print("Command Output:", result.stdout)
    res=result.stdout

    return res;



@app.route('/user', methods=['POST'])
def add_user():   
    data = request.get_json()

    # Extract username and password from request
    username = data.get('username')
    password = data.get('password')
    
    
    param = f"(record {{ \"username\" = \"{username}\"; \"password\" = \"{password}\" }})"
    print(param)
    command = [
    'dfx', 
    'canister', 
    'call', 
    'login-app-backend', 
    'addUser',
    param
    ]

    # Run the command and capture the output
    result = subprocess.run(command, capture_output=True, text=True)

    # Print the output of the command
    print("Command Output:", result.stdout)
    res=result.stdout

    return res;

@app.route('/user', methods=['GET'])
def get_user():   

    # Extract username and password from request
    
    
    param = f"()"
    print(param)
    command = [
    'dfx', 
    'canister', 
    'call', 
    'login-app-backend', 
    'listUsers',
    param
    ]

    # Run the command and capture the output
    result = subprocess.run(command, capture_output=True, text=True)

    # Print the output of the command
    print("Command Output:", result.stdout)
    res=result.stdout

    return res;

@app.route('/createtemplate', methods=['POST'])
def createtemplate():
    data = request.get_json()
    timestamp_ms = int(time.time() * 1000)
    # Extract username and password from request
    templatename = f"{data.get('username')}{timestamp_ms}"
    content = data.get('content')

    param = f"(record {{ \"templatename\" = \"{templatename}\"; \"content\" = \"{content}\" }})"
    print(param)
    command = [
    'dfx', 
    'canister', 
    'call', 
    'login-app-backend', 
    'addTemplate',
    param
    ]


    print("Command Input: dfx canister call login-app-backend addTemplate",param)
    # Run the command and capture the output
    result = subprocess.run(command, capture_output=True, text=True)

    # Print the output of the command
    print("Command Output:", result.stdout)
    res=result.stdout
    res=res.replace("(","").replace(")","").replace("\"{","{").replace("}\",","}").replace("\\","")
    dataresponse = json.loads(res)
    return dataresponse;

@app.route('/createpdfbytemplate', methods=['POST'])
def createpdfbytemplate():
    data = request.get_json()
    templatename= data.get('template_name') 
    parsingparam= data.get('parsing_param') 
    size= data.get('size') 
    # Extract username and password from request
    param = f"{templatename}"

    print(param)
    command = [
    'dfx', 
    'canister', 
    'call', 
    'login-app-backend', 
    'getTemplate',
    param
    ]


    print("Command Input: dfx canister call login-app-backend addTemplate",param)
    # Run the command and capture the output
    result = subprocess.run(command, capture_output=True, text=True)

    # Print the output of the command
    print("Command Output:", result.stdout)
    res=result.stdout
    res=res.replace("(","").replace(")","").replace(",","")
    # Decode the Base64 string
    decoded_bytes = base64.b64decode(res)

    # Convert bytes to a string (if applicable)
    html = decoded_bytes.decode("utf-8")

    results = parsingparam.split(",")
    for result in results:
        lines=result.split("|")
        html=html.replace(lines[0],lines[1])

    output_folder = "Output"  # Replace with your folder path
    output_file = os.path.join(output_folder, f"{templatename}.pdf")
    if data.get("size") == "A4":
        pdfkit.from_string(html, output_file,configuration=config,options=optionsA4)
    elif data.get("size" )== "A5":
        pdfkit.from_string(html, output_file,configuration=config,options=optionsA5)
        
    
    return f"https://8ac5-157-245-159-47.ngrok-free.app/viewpdf?file={templatename}.pdf"
    # dataresponse = json.loads(res)
    return res;


# Create PDF
@app.route('/createpdf', methods=['POST'])
def createpdf():
    data = request.get_json()
    # Extract username and password from request
    pages = data.get('pages')
    htmls=[]

    for page in pages:
        html_result="<html><head></head><body><table border=\"1\"><thead></thead><tbody>"
        lines=page.get('lines')
        for line in lines:
            html_result+="<tr>"
            columns=line.get('columns')
            value = ''
            for column in columns:
                value_type = column.get('type')
                style_str = column.get('style')
                width = "" if column.get('width', -1) == -1 else " width=\""+column.get('width')+"\" "
                height = "" if column.get('height', -1) == -1 else " height=\""+column.get('height')+"\""
                style_attribute = ""
                if value_type == 'text':
                    for s in style_str.split(","):
                        if s.lower() == 'bold':
                            style_attribute += "font-weight:bold;"
                        elif s.lower() == 'center':
                            style_attribute += "text-align:center;"
                        elif s.lower() == 'middle':
                            style_attribute += "vertical-align:middle;"
                    value = column.get('value')
                elif value_type == 'img':
                    for s in style_str.split(","):
                        if s == 'bold':
                            continue
                        style_attribute = f"align:{s};"
                    value = f"<img{width}{height} src={column.get('value')}>"
                    width, height = "", ""
                html_result+=f"<td{width}{height} style=\"{style_attribute}\" colspan=\"{column.get('colspan')}\">{value}</td>"
            html_result+="</tr>"
        html_result+="</tbody></table></body></html>"
        htmls.append(html_result)

    # Extract username and password from request
    print(htmls);
    # Save to a file
    t = int(time.time()*1000)
    output_folder = "Output"  # Replace with your folder path
    output_file = os.path.join(output_folder, f"output{data.get('username')}{t}.pdf")
    if data.get("size") == "A4":
        pdfkit.from_string(htmls[0], output_file,configuration=config,options=optionsA4)
    elif data.get("size" )== "A5":
        pdfkit.from_string(htmls[0], output_file, configuration=config,options=optionsA5)
    return f"https://8ac5-157-245-159-47.ngrok-free.app/viewpdf?file=output{data.get('username')}{t}.pdf"

# Get PDF
@app.route('/viewpdf', methods=['GET'])
def viewpdf():
    output_folder = "Output"  # Specify your folder path
    filename = request.args.get('file')  # Get the file name from query parameters
    output_file = os.path.join(output_folder, filename)  # Build full file path

    # Check if the file exists
    if os.path.exists(output_file):
        # Open the PDF file and convert it to base64
        with open(output_file, "rb") as pdf_file:
            encoded_pdf = base64.b64encode(pdf_file.read()).decode('utf-8')

        # Generate an HTML response to display the PDF
        html_content = f'''
        <html>
        <head><title>PDF Viewer</title></head>
        <body>
            <h1>PDF Viewer</h1>
            <iframe src="data:application/pdf;base64,{encoded_pdf}" width="100%" height="600px"></iframe>
        </body>
        </html>
        '''

        return render_template_string(html_content)
    else:
        return f"File not found: {output_file}", 404

# Get Sample
@app.route('/getsample', methods=['GET'])
def getsample():
    sample_folder = "Sample"  # Replace with your folder path
    sample_file = os.path.join(sample_folder, f"Sample.txt")
    file_path = sample_file
    json_data = read_file_as_json(file_path)

    return json_data

 
#internal methods
def read_file_as_json(file_path):
    try:
        with open(file_path, 'r') as file:
            data = json.load(file)  # Parse JSON content
            return data
    except FileNotFoundError:
        print(f"File not found: {file_path}")
    except json.JSONDecodeError:
        print(f"Error decoding JSON from file: {file_path}")
if __name__ == '__main__':
    app.run(host='0.0.0.0',port=5000)

