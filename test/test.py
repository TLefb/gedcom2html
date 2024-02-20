from gedcomParser import GedcomParser


# Define a class to hold and process individual's information
class Individual:
    def __init__(self, id, gender, name, birth_date, birth_place, death_date, death_place, marriage_date, marriage_place,
                 spouse_name, profession, father_name, mother_name, children, notes):
        self.id = id
        self.gender = gender
        self.name = name
        self.birth_date = birth_date
        self.birth_place = birth_place
        self.death_date = death_date
        self.death_place = death_place
        self.marriage_date = marriage_date
        self.marriage_place = marriage_place
        self.spouse_name = spouse_name
        self.profession = profession
        self.father_name = father_name
        self.mother_name = mother_name
        self.children = children  # This should be a list of children's names
        self.notes = notes  # This should be a list of children's names


# Assuming you have a way to parse your GEDCOM file, fill the individuals list with Individual objects.
individuals = []  # Populate this list with Individual objects based on your GEDCOM file.


# Function to generate HTML content for each individual
def generate_html(individual):
    # HTML template with CSS for layout
    html_template = f"""
    <html>
    <head>
        <title>{individual.name}</title>
        <meta charset="UTF-8"> <!-- Specify the character encoding for the HTML document -->
        <style>
            .container {{
                display: flex;
                flex-direction: column;
                align-items: center;
            }}
            .person-info {{
                display: flex;
                justify-content: space-between;
                width: 80%; /* Adjust based on preference */
                margin-bottom: 20px; /* Space between person-info and family-info */
            }}
            .images img {{
                width: 100px; /* Adjust image width as needed */
                height: auto;
            }}
            .info {{
                flex-grow: 1;
                margin: 0 20px; /* Adjust space between the text and images */
                text-align: left; /* Align person's information to the left */
            }}
            .family-info, .notes {{
                width: 80%; /* Match width of person-info for alignment */
                text-align: left; /* Align text to left */
                margin-bottom: 10px; /* Space between sections */
            }}
            hr {{
                width: 80%; /* Match width of other sections for alignment */
                border: 0;
                border-top: 1px solid #ccc; /* Style for horizontal line */
                margin: 20px 0; /* Space above and below the line */
            }}
        </style>
    </head>
    <body>
        <div class="container">
            <div class="person-info">
                <div class="images">
                    <img src="../image_gauche.jpg" alt="Left Image">
                </div>
                <div class="info">
                    <div class="name">{individual.name}</div>
                    <ul>
                        <li>Né le : {individual.birth_date} à {individual.birth_place}</li>
                        <li>Marié(e) le : {individual.marriage_date} avec {individual.spouse_name} à {individual.marriage_place}</li>
                        <li>Mort le : {individual.death_date} à {individual.death_place}</li>
                        <li>Profession: {individual.profession}</li>
                    </ul>
                </div>
                <div class="images">
                    <img src="../image_droite.jpg" alt="Right Image">
                </div>
            </div>
            <hr>
            <div class="family-info">
                <h3>Parents</h3>
                <p>Mère: {individual.mother_name if individual.mother_name else 'Unknown'}</p>
                <p>Père: {individual.father_name if individual.father_name else 'Unknown'}</p>
            </div>
            <hr>
            <div class="family-info">
                <h3>Enfants</h3>
                <ul>
                    {''.join(f"<li>{child}</li>" for child in individual.children)}
                </ul>
            </div>
            <hr>
            <div class="notes">
                <h3>Notes</h3>
                <p>{individual.notes}</p>
            </div>
        </div>
    </body>
    </html>
    """
    return html_template


# Main function to generate HTML files for each individual
def main():

    g = GedcomParser("LEFEBVRE.ged")
    all_persons = g.get_persons()
    id_list = list(all_persons.keys())
    id_list.sort()
    for _id in id_list:
        p = all_persons[_id]

        father_name = "?"
        mother_name = "?"
        spouse_name = "?"

        if len(p.parent_id) > 0:
            for parent_id in p.parent_id:
                if all_persons[parent_id].gender == "M":
                    father_name = f"{all_persons[parent_id].surname} {all_persons[parent_id].first_name}"
                if all_persons[parent_id].gender == "F":
                    mother_name = f"{all_persons[parent_id].surname} {all_persons[parent_id].first_name}"
        birth_date = p.birth_date.strftime('%d/%m/%Y') if p.birth_date is not False else "?"
        death_date = p.death_date.strftime('%d/%m/%Y') if p.death_date is not False else "?",

        children = []
        for index, family in enumerate(p.family):
            if len(family.spouse_id) > 0:
                spouse_name = f"{all_persons[family.spouse_id].surname} {all_persons[family.spouse_id].first_name}"
            if len(family.child_id) > 0:
                for child_id in family.child_id:
                    children.append(f"{all_persons[child_id].surname} {all_persons[child_id].first_name}")

        indiv = Individual(
            id=_id,
            gender=p.gender,
            name=f"{p.surname} {p.first_name}",
            birth_date=birth_date,
            birth_place=p.birth_place,
            death_date=death_date,
            death_place=p.death_place,
            marriage_date=p.current_marriage["date"] if p.current_marriage else "?",
            marriage_place=p.current_marriage["place"] if p.current_marriage else "?",
            spouse_name=spouse_name,
            profession=p.occupation,
            mother_name=mother_name,
            father_name=father_name,
            children=children,
            notes=p.notes
        )

        html_content = generate_html(indiv)
        filename = f"html/{p.id}.html"
        with open(filename, 'w', encoding='utf-8') as file:
            file.write(html_content)


# Run the main function
main()
