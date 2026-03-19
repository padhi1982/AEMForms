from bs4 import BeautifulSoup
import json

# MOCK AEM COMPONENT DATABASE
AEM_COMPONENT_MAP = {
    "text": "core/wcm/components/form/text",
    "email": "core/wcm/components/form/text (validation=email)",
    "checkbox": "core/wcm/components/form/options (type=checkbox)",
    "select": "core/wcm/components/form/options (type=drop-down)",
    "file": "core/wcm/components/form/upload"
}

def map_to_aem():
    # 1. Read the HTML
    with open("index.html", "r") as f:
        soup = BeautifulSoup(f, "html.parser")

    aem_spec = {
        "target_container": "/content/forms/af/my-headless-form",
        "components_to_create": []
    }

    # 2. Reverse Engineer
    form = soup.find("form")
    for input_tag in form.find_all(["input", "select"]):
        field_type = input_tag.name if input_tag.name == "select" else input_tag.get("type", "text")
        field_id = input_tag.get("id")
        
        # Map to AEM
        aem_component = AEM_COMPONENT_MAP.get(field_type, "core/wcm/components/form/text")

        aem_spec["components_to_create"].append({
            "field_id": field_id,
            "html_origin": f"<{input_tag.name} type='{field_type}'>",
            "aem_resource_type": aem_component,
            "status": "Ready for JCR content creation"
        })

    # 3. Output Spec
    with open("aem_spec_sheet.json", "w") as f:
        json.dump(aem_spec, f, indent=4)
    
    print("✅ Agent 3: AEM Specification Sheet generated.")

if __name__ == "__main__":
    map_to_aem()
