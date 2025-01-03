from flask import Flask, render_template, request, jsonify
import matplotlib.pyplot as plt
import numpy as np
import io
import base64

app = Flask(__name__)

def calculate_slt(synchronous_lecture, synchronous_activities, synchronous_assessment,
                   asynchronous_lecture, asynchronous_activities, asynchronous_assessment,
                   synchronous_lecture_prep, synchronous_activities_prep, synchronous_assessment_prep,
                   asynchronous_lecture_prep, asynchronous_activities_prep, asynchronous_assessment_prep):
    total_synchronous = (synchronous_lecture + synchronous_activities + synchronous_assessment +
                          synchronous_lecture_prep + synchronous_activities_prep + synchronous_assessment_prep)
    total_asynchronous = (asynchronous_lecture + asynchronous_activities + asynchronous_assessment +
                           asynchronous_lecture_prep + asynchronous_activities_prep + asynchronous_assessment_prep)
    total_slt = total_synchronous + total_asynchronous

    if total_slt != 120:
        warning = "Warning: Total SLT should be exactly 120 hours."
    else:
        warning = ""

    # Color logic: Red if < 36 hours or > 72 hours, Green otherwise
    if total_asynchronous < 36 or total_asynchronous > 72:
        bar_color = 'red'
    else:
        bar_color = 'green'

    # Generate plot
    fig, ax = plt.subplots()
    ax.bar(['Asynchronous Learning Hours'], [total_asynchronous], color=bar_color)
    ax.axhline(y=36, color='black', linestyle='--', label='Minimum 36 Hours')
    ax.axhline(y=72, color='black', linestyle='--', label='Maximum 72 Hours')
    ax.set_ylim(0, 120)  # Set limit to full 120 hours
    ax.set_ylabel("Hours of Asynchronous Learning")
    ax.set_title("Student Learning Time Distribution")
    ax.legend()

    # Convert plot to image
    img = io.BytesIO()
    plt.savefig(img, format='png')
    img.seek(0)
    graph_url = base64.b64encode(img.getvalue()).decode()
    plt.close(fig)

    return total_asynchronous, warning, graph_url

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        data = request.form
        total_asynchronous, warning, graph_url = calculate_slt(
            int(data['synchronous_lecture']), int(data['synchronous_activities']), int(data['synchronous_assessment']),
            int(data['asynchronous_lecture']), int(data['asynchronous_activities']), int(data['asynchronous_assessment']),
            int(data['synchronous_lecture_prep']), int(data['synchronous_activities_prep']), int(data['synchronous_assessment_prep']),
            int(data['asynchronous_lecture_prep']), int(data['asynchronous_activities_prep']), int(data['asynchronous_assessment_prep'])
        )
        return jsonify({'total_asynchronous': total_asynchronous, 'warning': warning, 'graph_url': graph_url})
    return render_template('index.html', developer_name="Developed by [Rohayati Paidi]")

if __name__ == '__main__':
    app.run(debug=True)
