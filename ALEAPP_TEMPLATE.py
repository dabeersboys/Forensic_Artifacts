#Update line 3-13
__artifacts_v2__ = {
    "ACME_Chats": {#UPDATE THE SCRIPT NAME. KEEP IT SMALL- CHANGING sChats
        "name": "ACME Chats and Calls",#WHAT IS YOUR NAME OF THE ARTIFACT
        "description": "Parses ACME Chat database",#DESCRIPTION OF THE ARTIFACT
        "author": "Matt Beers",#GIVE YOURSELF SOME CREDIT!
        "version": "0.0.1",
        "date": "2024-02-08",
        "requirements": "none",#AS LONG AS YOUR DOING A BASIC SQL QUERY YOU WON'T NEED THIS
        "category": "Chats",# IN ALEAPP THERE ARE A FEW CATEGORIES, KEEPING CHATS WILL GROUP THIS WITH OTHER IN THE CHAT CATEGORY
        "notes": "",# WHAT EVER NOTES YOU WANT TO ADD
        "paths": ('*/path/to/the/database.db*'),#VERY IMPORTANT, THIS IS THE PATH TO THE DATABASE YOU ARE PARSING. IF IT HAS A AN EXTENTSTION BE SURE TO INCLUDE IT. THE * LOOKS FOR OTHER FILES WITH THE NAME NAME BUT ADDITONAL EXTENTSTION LIKE -WAL -SHM -JOURNAL
        "function": "get_acmechats"#update line 22 to match this
    }
}

import sqlite3

from scripts.artifact_report import ArtifactHtmlReport
from scripts.ilapfuncs import logfunc, timeline, tsv, is_platform_windows, open_sqlite_db_readonly, convert_ts_human_to_utc, convert_utc_human_to_timezone

def get_acmechats(files_found, report_folder, seeker, wrap_text, time_offset):#your def variable should match what you have after function on line 13.
    
    data_list = []
    
    for file_found in files_found:
        file_found = str(file_found)
        
        if file_found.endswith('textfree'):
            db = open_sqlite_db_readonly(file_found)
            cursor = db.cursor()
            #SQL QUERY TIME! START YOUR QUERY AT THE SELECT STATEMENT. ITS A REQUIREMENT TO HAVE YOUR TIMESTAMPE FIRST FOR LEAPP ARTIFACTS
            cursor.execute('''
            SELECT
            datetime(conversation_item.timestamp / 1000, 'unixepoch', 'localtime') AS TIMESTAMP,
            contact_address.native_first_name,
            contact_address.native_last_name,
            CASE conversation_item.method
            WHEN '1' THEN 'Text'
            WHEN '3' THEN 'Call'
            WHEN '8' THEN 'Voicemail'
            ELSE 'Unknown'
            END AS method,
            conversation_item.message_text,
            conversation_item.duration,
            conversation_item.address
            FROM
            contact_address
            JOIN
            conversation_item ON contact_address.address_e164 = conversation_item.address
            ORDER BY
            conversation_item.timestamp DESC
            ''')

            all_rows = cursor.fetchall()
            usageentries = len(all_rows)
            if usageentries > 0:
                for row in all_rows:
                #    last_mod_date = row[0]
                #   if last_mod_date is None:
                #       pass
                #   else:
                #       last_mod_date = convert_utc_human_to_timezone(convert_ts_human_to_utc(last_mod_date),time_offset)
                
                    data_list.append((row[0],row[1],row[2],row[3],row[4],row[5],row[6]))#**IMPORTANT THIS IS FOR HOW MANY TABLES ARE LISTED IN YOUR QUERY. IS MORE THAN 7 ADD MORE ROW, IF LESS REMOVE ROW. ROW MUST START AT ROW 0
            db.close()
                    
        else:
            continue
        
    if data_list:
        description = 'ACME Chats and Calls' #THIS SHOWS UP ON THE REPORT SIDE
        report = ArtifactHtmlReport('ACME Chats')#THIS IS WHAT SHOWS UP ON THE RIGHT SIDE OF THE HTML REPORT
        report.start_artifact_report(report_folder, 'ACME Chats', description)
        report.add_script()
        data_headers = ('Timestamp','First Name','Last Name','Method','Message Text','Duration','Phone Number')#THIS IS WHERE YOU DEFINE THE COLUMN NAMES THAT SHOW UP IN THE REPORT AND SHOULD FOLLOW THE ORDER OF YOUR QUERY. 
        report.write_artifact_data_table(data_headers, data_list, file_found,html_escape=False)
        report.end_artifact_report()
        
        tsvname = 'ACME Chats'#UPDATE THIS TO MATCH YOUR ARTIFACT
        tsv(report_folder, data_headers, data_list, tsvname)
        
        tlactivity = 'ACME Chats'#UPDATE THIS TO MATCH YOUR ARTIFACT
        timeline(report_folder, tlactivity, data_list, data_headers)
    
    else:
        logfunc('No ACME data available')#if not found in extractions, this is where it logs it wasn't found. update the name.
