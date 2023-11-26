from flask import Flask, render_template, request

app = Flask(__name__)

import pymongo

# Connect to MongoDB
client = pymongo.MongoClient("mongodb+srv://userapp:userapp@cluster0.ofx0wrj.mongodb.net/?retryWrites=true&w=majority")  # Update with your MongoDB connection string
database = client["DrugBank"]  # Replace 'your_database_name' with your actual database name
collection = database["drugs"]  # Replace 'your_collection_name' with your actual collection name

def search_interactions(drug_names):
    # Search for interactions in the MongoDB collection
    result_drug1 = collection.find_one({"name": drug_names[0]})

    if result_drug1:
        # Assuming 'drug-interactions' is an array of objects with 'name' and 'description' attributes
        interactions1 = {interaction['name']: interaction['description'] for interaction in result_drug1.get('drug-interactions', [])}

        # Check if the second drug is in the interactions of the first drug
        interaction_description = interactions1.get(drug_names[1])

        if interaction_description:
            return {drug_names[1]: interaction_description}
    
    return None

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        drug_name1 = request.form['drug_name1']
        drug_name2 = request.form['drug_name2']

        # Search for drug interactions between the two drugs
        interaction_result = search_interactions([drug_name1, drug_name2])

        if interaction_result:
            interaction, description = interaction_result.popitem()
            result = f"Drug Interaction between {drug_name1} and {drug_name2}:\n- {interaction}: {description}"
        else:
            result = f"No interaction found between {drug_name1} and {drug_name2}"

        return render_template('index.html', result=result)

    return render_template('index.html')

if __name__ == "__main__":
    app.run(debug=True)

