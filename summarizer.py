import ollama
import os
from datetime import datetime

class TextSummarizer:

#This is the constructor method that Python runs automatically when you create a new instance of a class.
#It initializes the object with any default or passed-in values.
# model="mistral"
#This means that unless otherwise specified, the class will assume the model name is "mistral".
    def __init__(self, model="mistral"):    #self refers to the object being created
        self.model = model #Stores the model value inside the object, so the rest of the program can use it later.
        #Loads predefined prompt templates from a local prompts folder
        #This creates a path to a folder named prompts that lives in the same directory as the script.
        #__file__ is a built-in variable that gives you the current file's path.
        #os.path.dirname(__file__) gets the folder containing this file.
        #os.path.join(...) joins that folder path with 'prompts' to make a complete path.
        self.prompts_dir = os.path.join(os.path.dirname(__file__), 'prompts')
    

#load a specific prompt template from a file. Think of it as opening a notebook and pulling out just the section you want.
    def load_prompt_template(self,  template_name):
        """Load a prompt template from the prompts directory"""
        template_path = os.path.join(self.prompts_dir, 'prompt_templates.txt')  #This creates the full file path to a file named prompt_templates.txt

        #📖 Read the File
        try:
            #This opens the file for reading using UTF-8 encoding (to support all characters).
            with open(template_path, 'r', encoding='utf-8') as f:  #with open(...) as f ensures the file is automatically closed after reading.
                content = f.read() # reads all the file’s text into one big string.

                  # Simple template extraction
                templates = {}   #Creates an empty dictionary to store different templates by name.
                current_template = None #current_template keeps track of which template we're currently reading
                
                #Parse Each Line of the File
                for line in content.split('\n'):  #This splits the text into lines and processes each one
                    #If a line looks like [TemplateName], it’s the start of a new template.
                    #It saves the name inside the brackets and creates an empty string in the dictionary for it.
                    if line.startswith('[') and line.endswith(']'):
                        current_template = line[1:-1]
                        templates[current_template] = ""
                    #If we’re inside a template (i.e., current_template exists) and the line isn’t empty, it gets added to the corresponding template in the dictionary
                    elif current_template and line.strip():
                        templates[current_template] += line + "\n"
                return templates.get(template_name, "").strip()   #.strip() removes any leading/trailing whitespace or newlines.
        except FileNotFoundError:
            return "" 
        
#Combining prompt engineering with practical python
    #text: the input you want to summariz,
    # summary_type: the style of summary you want (default is 'brief'
    #max_length: optional—if given, it adds a word limit
    def summarize_text(self, text, summary_type="brief", maxlength = None):
        """
        Summarize text using different approaches
        
        Args:
            text (str): Text to summarize
            summary_type (str): 'brief', 'detailed', 'bullet_points', 'key_insights'
            max_length (int): Optional max length constraint
        """
    #This is a shortcut to insert the value of a variable directly into a string same like 'summarize_' + summary_type
        template = self.load_prompt_template(f'summarize_{summary_type}')

        if not template:    #if template not found"
            prompts = {
                'brief': "Summarize the following text in 2-3 sentences:",
                'detailed': "Provide a comprehensive summary of the following text, including main points and key details:",
                'bullet_points': "Summarize the following text as bullet points covering the main ideas:",
                'key_insights': "Extract the key insights and important takeaways from the following text:"
            }
            template = prompts.get(summary_type, prompts['brief'])  #get() ensures it falls back to 'brief' if the type isn’t recognized.
        
        if maxlength:
            template += f"\n\n Keep the summary under {maxlength} words"   #This appends a rule to keep the output short—perfect for tweets, captions, etc
#Combine Prompt with Input Text
        #This builds the full prompt that will be sent to the language model.
        #It blends the instruction (template) and the actual text
        prompt = f"{template}\n\nText to summarize:\n{text}"
        try:
            response = ollama.chat(
                model=self.model,
                messages=[
                    {'role': 'user', 'content': prompt}
                ]
            )
          
            return response['message']['content']  #Extracts the summarized text from the model’s response and gives it back to you.
        except Exception as e:
       
         return f"Error generating summary: {e}"

#summarize the contents of a text file
    def summarize_file(self, file_path, summary_type='brief'):
        """Summarize content from a text file"""
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                    content = f.read()
            return self.summarize_text(content, summary_type)
        except FileNotFoundError:
            return f"File not found: {file_path}"
        except Exception as e:
            return f"Error reading file: {e}"
        
#This batch_summarize method is all about processing multiple pieces of text and generating summaries for each one,
# which is super useful in real-world applications like summarizing emails, articles, reports, or even feedback lists.
    def batch_summarize(self, texts, summary_type = 'brief'):
        """Summarize multiple texts"""
        summaries = [] #Initializes an empty list to store the results (each result is a dictionary with the original and summarized content details).
        for i, text in enumerate(texts): #enumerate() is a super handy Python built-in function, especially when you're looping through a list and want to keep track of both the index and the value at the same time.
            print(f"Summarizing text {i+1}/{len(texts)}...")
            summary = self.summarize_text(text, summary_type) #as we used enumare no need of text[i]
            summaries.append({
                'original_length': len(text.split()),
                'summary': summary,
                'summary_length': len(summary.split())
            })
        return summaries
    
#🌟 This main() function ties everything you've built into a user-friendly, text-based menu system. It lets someone interactively choose what to summarize and how—like a little command-line app
def main():
        #creating an instance of your TextSummarizer class, which includes the summarize_text, summarize_file, and other methods
        summarizer = TextSummarizer()
        #just friendly banner
        print("Text Summarizer with Ollama")
        print("=" * 40)
    #Infinite Menu Loop
    #You’ve started an infinite loop—so the app keeps running until the user decides to quit. Inside it, you show:
        while True:
            print("\nShow options:")
            print("1. Summarize text input")
            print("2. Summarize from file")
            print("3. quit")

        #Ask for one
            choice =input("\n Enter your choice(1-3):").strip()

            if choice == "1":
                text = input("\n enter text to summarize:")

                #strip() This removes any whitespace
                #🚫 if not text.strip():
                # This checks if the cleaned-up string is empty
                # Continue tell python: “Ignore this input and wait for valid input instead.
                if not text.strip():
                    continue

                print("\nSummary types")
                print("\n1.Brief 2-3 sentences")
                print("\n2.Detailed:") 
                print("\n3.Bullet point")
                print("\n4.Key insights")
           
                type_choice = input("\n Choose Summary type(1-4)").strip()
                type_map = {'1': 'brief', '2': 'detailed', '3': 'bullet_points', '4': 'key_insights'}
                summary_type = type_map.get(type_choice, 'brief')

                print(f"\nGenerating {summary_type} summary..")
                summary = summarizer.summarize_text(text, summary_type)
                print(f"\n Summary {summary_type}:")
                print("_"*30)
                print(summary)
        
            elif choice == '2':
                file_path = input("\n Enter file path:").strip()
                summary_type = input("Enter summary type (brief/detailed/bullet_points/key_insights): ").strip() or 'brief'
    
                print('\nGenerating summary from file...')
                summary = summarizer.summarize_file(file_path, summary_type)
                print("\nFile Summary:")
                print("_" * 30)
                print(summary)

            elif choice == '3':
                print("Goodbye!")
                break
            else:
                print("Invalid choice , Try again.")

#if you import this summarizer.py , The main() function will not run automatically. You’d need to call it yourself using summary_app.main().
if __name__ == "__main__":   #Checks if the file is being run directly
    main()
    


