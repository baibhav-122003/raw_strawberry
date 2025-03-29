from importlib.resources.readers import remove_duplicates

import streamlit as st
import requests
import time
import json
import base64

FINAL_API_URL = "https://api.fabric.microsoft.com/v1/workspaces/28b51e78-d498-45f6-b9e8-6e22cc442754/dataPipelines?workspaceId=28b51e78-d498-45f6-b9e8-6e22cc442754"


AUTH_TOKEN = "Bearer eyJ0eXAiOiJKV1QiLCJhbGciOiJSUzI1NiIsIng1dCI6IkNOdjBPSTNSd3FsSEZFVm5hb01Bc2hDSDJYRSIsImtpZCI6IkNOdjBPSTNSd3FsSEZFVm5hb01Bc2hDSDJYRSJ9.eyJhdWQiOiJodHRwczovL2FwaS5mYWJyaWMubWljcm9zb2Z0LmNvbSIsImlzcyI6Imh0dHBzOi8vc3RzLndpbmRvd3MubmV0LzRhYzUwMTA1LTBjNjYtNDA0ZS1hMTA3LTdjYmQ4YTlhNjQ0Mi8iLCJpYXQiOjE3NDMyODc1MzAsIm5iZiI6MTc0MzI4NzUzMCwiZXhwIjoxNzQzMjkyNzI2LCJhY2N0IjowLCJhY3IiOiIxIiwiYWlvIjoiQVhRQWkvOFpBQUFBcjFmN2UrcmQ4RzU5N3dNdDlZQUc2UXB5ZW9lYmZUZzRPNUNvN2Z2UnVPTnFjSE8vT1RCQXYrb3NMd1BTUEZsRFJnblhDQ00wd1hIbWgwS0E5MExGT2tJV3BqN2R2Sk1laDNxVXgwYTg0WlZZckxLR0VodkZsRzhPdDVTVXI1WEUxdEhhSmZYTlp5T0ZmVzhWOXdBTmpBPT0iLCJhbXIiOlsicHdkIiwibWZhIl0sImFwcGlkIjoiMThmYmNhMTYtMjIyNC00NWY2LTg1YjAtZjdiZjJiMzliM2YzIiwiYXBwaWRhY3IiOiIwIiwiZmFtaWx5X25hbWUiOiJEZWJyb3kiLCJnaXZlbl9uYW1lIjoiQW5raXQiLCJpZHR5cCI6InVzZXIiLCJpcGFkZHIiOiIxNC45Ny4xNjQuNDYiLCJuYW1lIjoiQW5raXQgRGVicm95Iiwib2lkIjoiNGI4ZWJmYjYtODUxNC00YjBlLWEwODMtMDY4MjIzZGQwZWU0IiwicHVpZCI6IjEwMDMyMDA0MzhDODg1NDIiLCJyaCI6IjEuQVZZQUJRSEZTbVlNVGtDaEIzeTlpcHBrUWdrQUFBQUFBQUFBd0FBQUFBQUFBQUNmQUN0V0FBLiIsInNjcCI6IkFwcC5SZWFkLkFsbCBDYXBhY2l0eS5SZWFkLkFsbCBDYXBhY2l0eS5SZWFkV3JpdGUuQWxsIENvbm5lY3Rpb24uUmVhZC5BbGwgQ29ubmVjdGlvbi5SZWFkV3JpdGUuQWxsIENvbnRlbnQuQ3JlYXRlIERhc2hib2FyZC5SZWFkLkFsbCBEYXNoYm9hcmQuUmVhZFdyaXRlLkFsbCBEYXRhZmxvdy5SZWFkLkFsbCBEYXRhZmxvdy5SZWFkV3JpdGUuQWxsIERhdGFzZXQuUmVhZC5BbGwgRGF0YXNldC5SZWFkV3JpdGUuQWxsIEdhdGV3YXkuUmVhZC5BbGwgR2F0ZXdheS5SZWFkV3JpdGUuQWxsIEl0ZW0uRXhlY3V0ZS5BbGwgSXRlbS5FeHRlcm5hbERhdGFTaGFyZS5BbGwgSXRlbS5SZWFkV3JpdGUuQWxsIEl0ZW0uUmVzaGFyZS5BbGwgT25lTGFrZS5SZWFkLkFsbCBPbmVMYWtlLlJlYWRXcml0ZS5BbGwgUGlwZWxpbmUuRGVwbG95IFBpcGVsaW5lLlJlYWQuQWxsIFBpcGVsaW5lLlJlYWRXcml0ZS5BbGwgUmVwb3J0LlJlYWRXcml0ZS5BbGwgUmVwcnQuUmVhZC5BbGwgU3RvcmFnZUFjY291bnQuUmVhZC5BbGwgU3RvcmFnZUFjY291bnQuUmVhZFdyaXRlLkFsbCBUZW5hbnQuUmVhZC5BbGwgVGVuYW50LlJlYWRXcml0ZS5BbGwgVXNlclN0YXRlLlJlYWRXcml0ZS5BbGwgV29ya3NwYWNlLkdpdENvbW1pdC5BbGwgV29ya3NwYWNlLkdpdFVwZGF0ZS5BbGwgV29ya3NwYWNlLlJlYWQuQWxsIFdvcmtzcGFjZS5SZWFkV3JpdGUuQWxsIiwic2lkIjoiMDAzMjNiNzktNWQ0Yi01ZGUzLTI4MDMtNjUzZTE0MmQ5ZDk4Iiwic2lnbmluX3N0YXRlIjpbImttc2kiXSwic3ViIjoidDBQNlRYSHJfNWp4RV8zTGpQN3kyRVhhRlkyNy1ocjJ6TUU5Q3lIb0Y0ayIsInRpZCI6IjRhYzUwMTA1LTBjNjYtNDA0ZS1hMTA3LTdjYmQ4YTlhNjQ0MiIsInVuaXF1ZV9uYW1lIjoiYW5raXQuZEBTaWdtb2lkYW5hbHl0aWNzLmNvbSIsInVwbiI6ImFua2l0LmRAU2lnbW9pZGFuYWx5dGljcy5jb20iLCJ1dGkiOiI0eGs3TDk4YkowU1JvVUNqbzF3ekFBIiwidmVyIjoiMS4wIiwid2lkcyI6WyJiNzlmYmY0ZC0zZWY5LTQ2ODktODE0My03NmIxOTRlODU1MDkiXSwieG1zX2lkcmVsIjoiMSAyMCJ9.XD-t1QaO0t9fwjPiRgVjvALPDxV_Hv-dXaEoUPic4wEV_YxCwPYGMsPYYjJqKhGoJx1u0ozvJHFxlMyGq9qNVpyT50UwrV6lVNJzO1Sn--iq4IuXLQt0L13BUc9zSRRtbrPcM6GeExlCBuKpvZxKZE5kgExrcphiZPA1dj8gBdsKsC-SAS6QWasPXBNFrLhsXu4Ppiqa8DeVJH8KZh6jozBQHOC7RQtQHLlLxvUnMplZK8WjiZePihkZ_k0nfep_T5IRzcFKWbKXrHEEs9EPD5Gu9MoImuM8oLKgyUL5PwazUdtcY2eE4v28XOGnDS_1maB4aKhSSh7JADfmjL1ptQ"



if "pipeline_name" not in st.session_state:
    st.session_state["pipeline_name"] = ""


remove_nulls = False
remove_duplicates = False
selected_table = None
output_table = None



def json_to_base64(json_Def):
    json_string = json.dumps(json_Def)
    base64_encoded_string = base64.b64encode(json_string.encode('utf-8')).decode('utf-8')

    return base64_encoded_string

def call_adf_api(endpoint, payload=None):
    headers = {
        "Authorization": AUTH_TOKEN,  
        "Content-Type": "application/json"
    }
    response = requests.get(endpoint, headers=headers)
    return response.json()

# Initialize session state for page navigation if not already set.
if "page" not in st.session_state:
    st.session_state["page"] = "Select Data Source"

# UI Title with Strawberry Icon
st.markdown("<h1 style='text-align: center; font-size: 50px;'>_project🍓</h1>", unsafe_allow_html=True)



######################
# Page 1: Data Source Selection
######################
if st.session_state["page"] == "Select Data Source":
    
    # Ask for Pipeline Name first (value is automatically stored in st.session_state with key "pipeline_name")

    st.title("Select Data Source")
    data_source = st.selectbox("Choose a Data Source", ["Onelake"])
    
    if st.button("Confirm Selection"):
        response = call_adf_api("https://api.fabric.microsoft.com/v1/workspaces/28b51e78-d498-45f6-b9e8-6e22cc442754/lakehouses/c347f46e-9c07-4a77-b726-2bbf4639511e/tables")
        st.session_state["table_data"] = response
        st.success("Data source confirmed. Now select a table.")
    
    if "table_data" in st.session_state:
        table_data = st.session_state["table_data"]
        table_names = [table["name"] for table in table_data.get("data", [])]
        selected_table = st.selectbox("Select a Table", table_names)
        if st.button("Next"):
            st.session_state["selected_table"] = selected_table
            st.session_state["page"] = "Data Cleaning"
            st.rerun()
    
######################
# Page 2: Data Cleaning
######################
elif st.session_state["page"] == "Data Cleaning":
    st.title("Data Cleaning")
    if "selected_table" in st.session_state:
        st.write(f"Cleaning table: {st.session_state['selected_table']}")
    else:
        st.error("Please select a table first in the 'Select Data Source' page.")
        st.stop()
    
    # Checkboxes for Cleaning Options
    remove_duplicates = st.checkbox("Remove Duplicates")
    remove_nulls = st.checkbox("Handle Null Values")
    st.session_state["remove_duplicates"] = remove_duplicates
    st.session_state["remove_nulls"] = remove_nulls

    col1, col2 = st.columns(2)
    with col1:
        if st.button("Back"):
            st.session_state["page"] = "Select Data Source"
            st.rerun()
    with col2:
        if st.button("Next"):
            st.session_state["page"] = "Data Transformation"
            st.rerun()

######################
# Page 3: Data Transformation
######################
elif st.session_state["page"] == "Data Transformation":
    st.title("Data Transformation")
    
    if "selected_table" not in st.session_state:
        st.error("Please select a table first in the 'Select Data Source' page.")
        st.stop()
    
    st.write(f"Transforming table: {st.session_state['selected_table']}")
    
    # Define available columns based on table name
    column_mapping = {
        "Student_Data": ["ID", "Standard", "Subject"],
        "Cars_data": ["Brand", "Model", "Year", "Fuel", "Transmission"],
        "Customer": ["First_Name", "Last_Name", "Birth_Date"]
    }
    selected_table = st.session_state["selected_table"]
    available_columns = column_mapping.get(selected_table, [])
    
    # Initialize transformations list in session state if not exists
    if "transformations" not in st.session_state:
        st.session_state["transformations"] = []
    
    # Transformation type selection
    transformation_options = ["Filter Data", "Remove Column"]
    selected_transformation = st.selectbox("Choose Transformation", transformation_options)
    
    if selected_transformation == "Filter Data":
        st.subheader("Add Filter Transformation")
        filter_column = st.selectbox("Select Column to Filter", available_columns, key="filter_column")
        # Operator dropdown is disabled and preset to 'equals'
        operator = st.selectbox("Operator", ["equals"], disabled=True, key="operator")
        filter_value = st.text_input("Value", key="filter_value")
        if st.button("Add Filter"):
            transformation = {
                "type": "Filter",
                "column": filter_column,
                "operator": operator,
                "value": filter_value
            }
            st.session_state["transformations"].append(transformation)
            st.success("Filter added.")
            st.rerun()
    
    elif selected_transformation == "Remove Column":
        st.subheader("Add Remove Column Transformation")
        remove_columns = st.multiselect("Select Columns to Remove", available_columns, key="remove_columns")
        if st.button("Add Remove Column"):
            transformation = {
                "type": "Remove Column",
                "columns": remove_columns
            }
            st.session_state["transformations"].append(transformation)
            st.success("Remove Column transformation added.")
            st.rerun()
    
    st.write("### Transformations Added:")
    if st.session_state["transformations"]:
        for idx, trans in enumerate(st.session_state["transformations"]):
            col_text, col_delete = st.columns([9, 1])
            with col_text:
                if trans["type"] == "Filter":
                    st.write(f"{idx+1}. Filter: {trans['column']} {trans['operator']} {trans['value']}")
                elif trans["type"] == "Remove Column":
                    st.write(f"{idx+1}. Remove Columns: {', '.join(trans['columns'])}")
            with col_delete:
                if st.button("🗑️", key=f"delete_{idx}"):
                    st.session_state["transformations"].pop(idx)
                    st.rerun()
    else:
        st.write("No transformations added yet.")
    
    # Navigation buttons: Back and Apply Transformations
    col1, col2 = st.columns(2)
    with col1:
        if st.button("Back"):
            st.session_state["page"] = "Data Cleaning"
            st.rerun()
    with col2:
        if st.button("Apply Transformations"):
            st.success("Transformations Applied!")
            st.session_state["show_next"] = True
            st.rerun()
    
    if st.session_state.get("show_next"):
        if st.button("Next"):
            st.session_state["page"] = "Load Data"
            st.session_state.pop("show_next")
            st.rerun()

######################
# Page 4: Load Data
######################
elif st.session_state["page"] == "Load Data":
    st.title("Load Data")
    data_destination = st.selectbox("Choose Data Destination", ["Onelake"], key="destination")
    output_table = st.text_input("Output Table Name", key="output_table")
    pipeline_name = st.text_input("Enter Pipeline Name", key="pipeline_name")

    if st.button("Confirm"):
        st.session_state["data_destination"] = data_destination

        filter_transformations = [
            t for t in st.session_state.get("transformations", []) if t.get("type") == "Filter"
        ]

        remove_column_transformations = [
            t for t in st.session_state.get("transformations", []) if t.get("type") == "Remove Column"
        ]

        parameters = {}

        if remove_column_transformations:
            parameters["remove_column"] = {
                "value": remove_column_transformations[0]["columns"][0],
                "type": "string"
            }

        if filter_transformations:
            parameters["filter_column_value"] = {
                "value": f"{filter_transformations[0]['column']}:{filter_transformations[0]['value']}",
                "type": "string"
            }

        pipeline_definition = {
            "properties": {
                "activities": [
                    {
                        "name": "Extract",
                        "type": "Copy",
                        "dependsOn": [],
                        "policy": {
                            "timeout": "0.12:00:00",
                            "retry": 0,
                            "retryIntervalInSeconds": 30,
                            "secureOutput": "false",
                            "secureInput": "false"
                        },
                        "typeProperties": {
                            "source": {
                                "type": "LakehouseTableSource",
                                "datasetSettings": {
                                    "annotations": [],
                                    "linkedService": {
                                        "name": "strawlake",
                                        "properties": {
                                            "annotations": [],
                                            "type": "Lakehouse",
                                            "typeProperties": {
                                                "workspaceId": "28b51e78-d498-45f6-b9e8-6e22cc442754",
                                                "artifactId": "c347f46e-9c07-4a77-b726-2bbf4639511e",
                                                "rootFolder": "Tables"
                                            }
                                        }
                                    },
                                    "type": "LakehouseTable",
                                    "schema": [],
                                    "typeProperties": {
                                        "table": st.session_state["selected_table"]
                                    }
                                }
                            },
                            "sink": {
                                "type": "LakehouseTableSink",
                                "tableActionOption": "OverwriteSchema",
                                "partitionOption": "None",
                                "datasetSettings": {
                                    "annotations": [],
                                    "linkedService": {
                                        "name": "strawlake_inter",
                                        "properties": {
                                            "annotations": [],
                                            "type": "Lakehouse",
                                            "typeProperties": {
                                                "workspaceId": "28b51e78-d498-45f6-b9e8-6e22cc442754",
                                                "artifactId": "d7689f98-b30a-45b9-b58f-b6b9f7fd62fb",
                                                "rootFolder": "Tables"
                                            }
                                        }
                                    },
                                    "type": "LakehouseTable",
                                    "schema": [],
                                    "typeProperties": {
                                        "table": "Extracted_Data"
                                    }
                                }
                            },
                            "enableStaging": "false",
                            "translator": {
                                "type": "TabularTranslator",
                                "typeConversion": "true",
                                "typeConversionSettings": {
                                    "allowDataTruncation": "true",
                                    "treatBooleanAsNumber": "false"
                                }
                            }
                        }
                    },
                    {
                        "name": "Cleaning",
                        "type": "TridentNotebook",
                        "dependsOn": [
                            {
                                "activity": "Extract",
                                "dependencyConditions": [
                                    "Succeeded"
                                ]
                            }
                        ],
                        "policy": {
                            "timeout": "0.12:00:00",
                            "retry": 0,
                            "retryIntervalInSeconds": 30,
                            "secureOutput": "false",
                            "secureInput": "false"
                        },
                        "typeProperties": {
                            "notebookId": "abeab06f-1b94-4f3e-a548-5c03f0837fd1",
                            "workspaceId": "28b51e78-d498-45f6-b9e8-6e22cc442754",
                            "parameters": {
                                "remove_nulls": {
                                    "value": "True" if st.session_state["remove_nulls"] else "False",
                                    "type": "bool"
                                },
                                "remove_duplicates": {
                                    "value": "True" if st.session_state["remove_duplicates"] else "False",
                                    "type": "bool"
                                }
                            }
                        }
                    },
                    {
                        "name": "Transformation",
                        "type": "TridentNotebook",
                        "dependsOn": [
                            {
                                "activity": "Cleaning",
                                "dependencyConditions": [
                                    "Succeeded"
                                ]
                            }
                        ],
                        "policy": {
                            "timeout": "0.12:00:00",
                            "retry": 0,
                            "retryIntervalInSeconds": 30,
                            "secureOutput": "false",
                            "secureInput": "false"
                        },
                        "typeProperties": {
                            "notebookId": "d831038e-8c67-4b11-ba39-ea50cfad8a22",
                            "workspaceId": "28b51e78-d498-45f6-b9e8-6e22cc442754",
                            "parameters": parameters
                        }
                    },
                    {
                        "name": "Load",
                        "type": "Copy",
                        "dependsOn": [
                            {
                                "activity": "Transformation",
                                "dependencyConditions": [
                                    "Succeeded"
                                ]
                            }
                        ],
                        "policy": {
                            "timeout": "0.12:00:00",
                            "retry": 0,
                            "retryIntervalInSeconds": 30,
                            "secureOutput": "false",
                            "secureInput": "false"
                        },
                        "typeProperties": {
                            "source": {
                                "type": "LakehouseTableSource",
                                "datasetSettings": {
                                    "annotations": [],
                                    "linkedService": {
                                        "name": "strawlake_inter",
                                        "properties": {
                                            "annotations": [],
                                            "type": "Lakehouse",
                                            "typeProperties": {
                                                "workspaceId": "28b51e78-d498-45f6-b9e8-6e22cc442754",
                                                "artifactId": "d7689f98-b30a-45b9-b58f-b6b9f7fd62fb",
                                                "rootFolder": "Tables"
                                            }
                                        }
                                    },
                                    "type": "LakehouseTable",
                                    "schema": [],
                                    "typeProperties": {
                                        "table": "Transformed_Data"
                                    }
                                }
                            },
                            "sink": {
                                "type": "LakehouseTableSink",
                                "tableActionOption": "Append",
                                "partitionOption": "None",
                                "datasetSettings": {
                                    "annotations": [],
                                    "linkedService": {
                                        "name": "strawlake",
                                        "properties": {
                                            "annotations": [],
                                            "type": "Lakehouse",
                                            "typeProperties": {
                                                "workspaceId": "28b51e78-d498-45f6-b9e8-6e22cc442754",
                                                "artifactId": "c347f46e-9c07-4a77-b726-2bbf4639511e",
                                                "rootFolder": "Tables"
                                            }
                                        }
                                    },
                                    "type": "LakehouseTable",
                                    "schema": [],
                                    "typeProperties": {
                                        "table": st.session_state["output_table"]
                                    }
                                }
                            },
                            "enableStaging": "false",
                            "translator": {
                                "type": "TabularTranslator",
                                "typeConversion": "true",
                                "typeConversionSettings": {
                                    "allowDataTruncation": "true",
                                    "treatBooleanAsNumber": "false"
                                }
                            }
                        }
                    }
                ],
                "lastModifiedByObjectId": "8cec6a79-5f08-490b-9433-857a104ee019",
                "lastPublishTime": "2025-03-29T20:08:19Z"
            }
        }

        pipeline_definition_base64 = json_to_base64(pipeline_definition)
        headers = {
            "Authorization": AUTH_TOKEN,
            "Content-Type": "application/json"
        }
        print(st.session_state["pipeline_name"])
        payload = {
            "displayName": st.session_state["pipeline_name"],
            "description": "A data pipeline description",
            "definition": {
                "parts": [
                    {
                        "path": "pipeline-content.json",
                        "payload": pipeline_definition_base64,
                        "payloadType": "InlineBase64"
                    }
                ]
            }
        }
        response = requests.post(FINAL_API_URL, json=payload, headers=headers)
        print(response)

        # with st.spinner("Creating Data Pipeline..."):
        #     try:
        #         response = requests.post(FINAL_API_URL, json=payload, headers=headers)
        #         for chunk in response.iter_content(chunk_size=1024):
        #             if chunk:
        #                 pass  # Keep waiting until the response is fully received
        #         if response.status_code == 201:
        #             st.session_state["page"] = "Pipeline Success"
        #         else:
        #             st.error(f"Failed to create pipeline: {response.text}")
        #     except Exception as e:
        #         st.error(f"An error occurred: {e}")
        # st.rerun()

# ######################
# # Page 5: Pipeline Success
# ######################
# elif st.session_state["page"] == "Pipeline Success":
#     st.balloons()
#     st.success("🎉 Data Pipeline Created Successfully! 🎉")
#     if st.button("Okay"):
#         st.session_state["page"] = "Pipeline Final"
#         st.rerun()

# ######################
# # Page 6: Pipeline Final (New Pipeline Option)
# ######################
# elif st.session_state["page"] == "Pipeline Final":
#     st.title("Data Pipeline Completed")
#     if st.button("Create New Pipeline"):
#         st.session_state.clear()
#         st.session_state["page"] = "Select Data Source"
#         st.rerun()
