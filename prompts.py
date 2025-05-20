"""
Prompt templates and generation functions for abstract analysis.
"""

from typing import Dict, Optional


def generate_abstract_analysis_prompt(text: str) -> str:
    """
    Generate a prompt for analyzing an abstract to extract features and correlations.
    
    Args:
        text: The abstract text to analyze
        
    Returns:
        A formatted prompt string
    """
    return f""" 
    Define the following key variables for the extraction process: 
    
    1. **GEOGRAPHIC**: The **GEOGRAPHIC** refers to the **geographical scope** or **area of study** under study.  
    - If the abstract mentions a specific region, **country**, or **city** such as **deprived neighbourhoods**, specific **countries**, or **cities**, specify this. 
    - If no geographical scope is mentioned, label it as "None". 
    
    2. **ITEM**: The specific practice, choice, lifestyle, public policy, private action, property, feature, technological device, system, or service mentioned in the abstract.  
    **ITEM** cannot be a metric, measure, methods, or model. It refers to concrete actions, policies, features, or devices described in the text. 
    It should include the sense of variation of the **ITEM** (**increasing**, **lower**, **diminish**, etc.).  
    The **ITEM** should be complete and as detailed as possible, extracting all relevant aspects from the abstract (for instance, if the abstract analyses the "European regulation" **ITEM** must report on what it applies (example: transport safety), if etc.). 
    
    **Examples of ITEM**: 
    - **Practices, choices, behaviors, and lifestyles**: biking, carpooling, car-free lifestyle, teleworking. 
    - **Public policies or private actions**: carbon tax, transit infrastructure investment, reduced traffic zoning, corporate mobility plan, car weight reduction. 
    - **Properties and features of the built environment and cities**: sidewalks width, bike lanes investment, urban density, walkability, infrastructure. 
    - **Spatial distribution of urban amenities and location mismatches**: spatial mismatch, job accessibility, home-work separation, urban growth, sprawling development, residential specialization. 
    - **Technical or technological devices, systems, and services**: electric scooter sharing, bus rapid transit, microcars, trolleybus, tram systems.

    3. **FACTOR**: The **FACTOR** refers to the specific outcome or characteristic that the **ITEM** impacts or influences. This could be a variable, metric, or property, such as CO2 emissions, energy use, health outcomes, traffic congestion, car dependency, food or job accessibility, income inequalities, or land use.  
    - **FACTOR** cannot include negative formulations like "decrease", "reduction", "lowering", "savings", or "loss of". If the **FACTOR** is presented negatively in the abstract, it should be rephrased positively (e.g., "CO2 emission reduction" should be framed as "CO2 emissions", the reduction part would be included in the **CORRELATION**). 
    - **FACTOR** can also be an **ITEM** in the context of other **ITEMs**. In other words, an **ITEM** can act as a **FACTOR** for another **ITEM** if it influences or affects it. For example, **public transport** (an **ITEM**) can affect **CO2 emissions** (a **FACTOR**), but **CO2 emissions** can also be impacted by another **ITEM** like **carpooling**. Therefore, when extracting **ITEMs** and **FACTORS**, be aware that **ITEMs** can also act as **FACTORS** for other **ITEMs**. 

    4. **CORRELATION**: The **CORRELATION** describes the nature of the relationship between the **ITEM** and the **FACTOR**: 
    - If the **ITEM** is **increasing** or **raising** the **FACTOR**, label it as "increasing". 
    - If the **ITEM** is **reducing**, **diminishing**, or **lowering** the **FACTOR**, label it as "decreasing". 
    - If the **ITEM** has a **neutral impact** on the **FACTOR**, label it as "neutral". 
    - If the **ITEM** has an **unspecified** effect, label it as "None". 

    5. **POPULATION**: The **POPULATION** refers to the specific **socio-demographic group** affected by the **FACTOR**.   
    - If the abstract mentions a specific socio-demographic group, such as people in **elderly**, **young**, **low-income households**, **first decile**, **suburban households**, **peripheral**, etc., specify this. 
    - If no socio-demographic group is mentioned, label it as "None". 

    6. **MODE**: The **MODE** refers to the specific modes of transportation related to the **ITEM** and mentioned in the abstract.   
    - If the abstract mentions transportation modes, such as **bus**, **car**, **bike**, **bike-sharing**, **public transport**, **electric scooter**, **automobile**, etc., please specify it. 
    - If no **mode of transport** is **clearly** mentioned, leave it as "None". 

    7. **ACTOR**: The **ACTOR** refers to the institution or person directly effecting the **ITEM** and mentioned in the abstract.  
    - If the abstract mentions, such as **government**, **local authority**, **car manufacturer**, **firm**, **individual** etc., please specify it.  
    - If no actor is **clearly** mentioned, leave it as "None".  

    --- 

    Now, analyze the following abstract and: 
    1. Identify the **GEOGRAPHIC** scope of the study (if mentioned in the abstract). If not, label it as "None". 
    2. Extract all the **ITEMs** mentioned. If **no ITEMs** are found in the abstract, return **None** and stop the prompt. 
    3. For each extracted **ITEM**, determine whether it has a **increasing**, **decreasing**, or **neutral** effect on one or more **FACTORS**. Extract the impacted **FACTORS** (write "None" if no factors are impacted). 
    4. For each **ITEM** and its associated **FACTOR**, specify the **CORRELATION** as stated in the abstract.  
    5. If the **FACTOR** applies to a specific **POPULATION**, specify it as **POPULATION**. 
    6. If the **ITEM** is related to a specific **MODE** of transportation, specify it. 
    7. If the **ITEM** is related to a specific **ACTOR**, specify it. 

    **Do not make any assumptions or infer data for items that are not mentioned in the abstract.** 
    **Do not use acronyms if the developed formulation is in the abstract.**

    Return the extracted information in the following JSON format: 

    {{ 
        "GEOGRAPHIC": "new towns", 
        "transit infrastructure investment": {{ 
            "ACTOR": "urban planner", 
            "MODE": "None", 
            "POPULATION": "None", 
            "FACTOR": {{ 
                "social exclusion": {{ 
                    "CORRELATION": "decreasing", 
                }}, 
                "CO2 emissions": {{ 
                    "CORRELATION": "decreasing", 
                }} 
            }} 
        }}, 
        "microcars": {{ 
            "ACTOR": "car manufacturer", 
            "MODE": "car", 
            "POPULATION": "elderly", 
            "FACTOR": {{ 
                "materials use": {{ 
                    "CORRELATION": "decreasing", 
                }}, 
                "food accessibility": {{ 
                    "CORRELATION": "increasing", 
                }} 
            }} 
        }}, 
        ... 
    }} 


    **The above labels are only examples of the data format. Do **not** include them in your response. The extracted data should use the actual **ITEM** and **FACTOR** names as they appear in the abstract.** 

    The output should **not** start with the word "json" or include any other labels outside of the JSON format. 

    Abstract: {text} 
    """
    
    
def prompt_without_correlation(text: str) -> str:
    """
    Generate a prompt for analyzing an abstract to extract features and correlations.
    """
    return f""" 
    Define the following key variables for the extraction process: 
    
    1. **GEOGRAPHIC**: The **GEOGRAPHIC** refers to the **geographical scope** or **area of study** under study.  
    - If the abstract mentions a specific region, **country**, or **city** such as **deprived neighbourhoods**, specific **countries**, or **cities**, specify this. 
    - If no geographical scope is mentioned, label it as "None". 
    
    2. **ITEM**: The specific practice, choice, lifestyle, public policy, private action, property, feature, technological device, system, or service mentioned in the abstract.  
    **ITEM** cannot be a metric, measure, methods, or model. It refers to concrete actions, policies, features, or devices described in the text. 
    It should include the sense of variation of the **ITEM** (**increasing**, **lower**, **diminish**, etc.).  
    The **ITEM** should be complete and as detailed as possible, extracting all relevant aspects from the abstract (for instance, if the abstract analyses the "European regulation" **ITEM** must report on what it applies (example: transport safety), if etc.). 
    
    **Examples of ITEM**: 
    - **Practices, choices, behaviors, and lifestyles**: biking, carpooling, car-free lifestyle, teleworking. 
    - **Public policies or private actions**: carbon tax, transit infrastructure investment, reduced traffic zoning, corporate mobility plan, car weight reduction. 
    - **Properties and features of the built environment and cities**: sidewalks width, bike lanes investment, urban density, walkability, infrastructure. 
    - **Spatial distribution of urban amenities and location mismatches**: spatial mismatch, job accessibility, home-work separation, urban growth, sprawling development, residential specialization. 
    - **Technical or technological devices, systems, and services**: electric scooter sharing, bus rapid transit, microcars, trolleybus, tram systems.

    3. **FACTOR**: The **FACTOR** refers to the specific outcome or characteristic that the **ITEM** impacts or influences. This could be a variable, metric, or property, such as CO2 emissions, energy use, health outcomes, traffic congestion, car dependency, food or job accessibility, income inequalities, or land use.  
    - **FACTOR** cannot include negative formulations like "decrease", "reduction", "lowering", "savings", or "loss of". If the **FACTOR** is presented negatively in the abstract, it should be rephrased positively (e.g., "CO2 emission reduction" should be framed as "CO2 emissions", the reduction part would be included in the **CORRELATION**). 
    - **FACTOR** can also be an **ITEM** in the context of other **ITEMs**. In other words, an **ITEM** can act as a **FACTOR** for another **ITEM** if it influences or affects it. For example, **public transport** (an **ITEM**) can affect **CO2 emissions** (a **FACTOR**), but **CO2 emissions** can also be impacted by another **ITEM** like **carpooling**. Therefore, when extracting **ITEMs** and **FACTORS**, be aware that **ITEMs** can also act as **FACTORS** for other **ITEMs**. 

    --- 

    Now, analyze the following abstract and: 
    1. Identify the **GEOGRAPHIC** scope of the study (if mentioned in the abstract). If not, label it as "None". 
    2. Extract all the **ITEMs** mentioned. If **no ITEMs** are found in the abstract, return **None** and stop the prompt. 
    3. For each extracted **ITEM**, determine whether it has a **increasing**, **decreasing**, or **neutral** effect on one or more **FACTORS**. Extract the impacted **FACTORS** (write "None" if no factors are impacted). 
    4. For each **ITEM** and its associated **FACTOR** and summarize the correlation between the **ITEM** and the **FACTOR** in a single simple sentence named **CORRELATION**.

    **Do not make any assumptions or infer data for items that are not mentioned in the abstract.** 
    **Do not use acronyms if the developed formulation is in the abstract.**

    Abstract: {text} 
    """ 
