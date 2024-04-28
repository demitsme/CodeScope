import json

allowed_lang = ['GNU C++11', 'GNU C++14', 'MS C++', 'GNU C++0x', 'GNU C++', 'MS C++ 2017', 'Clang++17 Diagnostics', 'GNU C++17', 'MS C#', 'Mono C#', '.NET Core C#', 'Java 11', 'Java 7', 'Java 6', 'Java 8', 'JavaScript', 'Node.js', 'GNU C', 'GNU C11', 'Python 2', 'PyPy 3', 'Python 3', 'PyPy 2', 'PHP', 'Ruby', 'Kotlin', 'Rust', 'Go']
# Open the JSONL file
with open('program_synthesis/inference/results/program_synthesis_run_palm.jsonl', 'r') as file, open('program_synthesis/inference/your_codes/your_codes.jsonl', 'w') as output_file:
    # Iterate over each line
    for line in file:
        # Parse each line as JSON
        data = json.loads(line)

        # Extract relevant fields
        lang_cluster = data["lang_cluster"]
        src_uid = data["src_uid"]
        difficulty = data["difficulty"]
        testcases = data["testcases"]

        if lang_cluster == "D" or lang_cluster == "Delphi" or lang_cluster == "Perl" : continue

        # Loop within each program_synthesis from 0 to 4
        for i in range(5):  # Range from 0 to 4 (inclusive)
            # Extract specific program_synthesis entry
            program_synthesis_key = f"program_synthesis_{i}"
            raw_prog = data.get(program_synthesis_key)  # Get source code or empty string if not found

            if raw_prog == "" : continue

            version_start = raw_prog.find('"version": "') + len('"version": "')
            version_end = raw_prog.find('",', version_start)
            source_code_start = raw_prog.find('"target code": "') + len('"target code": "')
            source_code_end = raw_prog.find('"', source_code_start)

            # Extract version and source code
            # '"' + source_code + '"'
            version = raw_prog[version_start:version_end]
            if lang_cluster == "PHP" or lang_cluster == "Ruby" or lang_cluster == "Kotlin" or lang_cluster == "Rust" or lang_cluster == "Go":
                version = lang_cluster
            if version not in allowed_lang : continue
            source_code = raw_prog[source_code_start:source_code_end] 

            # Format data into desired format
            formatted_data = {
                "lang_cluster": lang_cluster,
                "lang": version,
                "source_code": source_code,
                "src_uid": src_uid,
                "difficulty": difficulty,
                "testcases": testcases
            }

            # print(program_synthesis_key, version)
            # print('---------------------------------------------------')
            output_file.write(json.dumps(formatted_data) + '\n')