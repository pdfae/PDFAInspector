import org.mozilla.javascript.*;
import org.mozilla.javascript.optimizer.*;
import java.io.*;

import com.itextpdf.*;

/**
 * Reads in Json Formatted pdf File
 * Reads in Json formatted rules
 */
public class RulesProcessor extends Shell{
	
	public enum JSFileType{
		FormalRules, PDFObj
	}

	// File to write all processing output to
	static String outFile;
	// BufferedWriter is an output stream that will write to the file above
	// static BufferedWriter outResults;
	PrintWriter outResults;
	
	// This is the string that will be written to file each time print is called
	static String toWrite;
	// This file is intermediate for processing all javascript at once
	static String intermediate = "files/JS.txt";
	// Variable that keeps track of what javascript file is being processed
	JSFileType jsFileType = JSFileType.FormalRules;
	
	// current directory on webserver where Processor.txt and Rules.txt exist
	String webServerDirectory = "/var/www/django/pdfainspector/web/files/";
	
	public void runRules(String jsonObjIn, String pathname, String filename)
	{
		System.out.println("runRules function called");
		outFile = pathname + filename;
		intermediate = pathname + "JS.txt";
		
		try{
			System.out.println("entering try statement");
			String instr;
			BufferedReader in1 = new BufferedReader(new FileReader(jsonObjIn));
			System.out.println("read json object file");
			BufferedReader in2 = new BufferedReader(new FileReader("files/Processor.txt"));
			System.out.println("read processor file");
			BufferedReader in3 = new BufferedReader(new FileReader("files/Rules.txt"));
			System.out.println("read rules file");
			BufferedWriter outIntermediate = new BufferedWriter(new FileWriter(intermediate));
			System.out.println("creating json file writer and writing to it");
			
			outIntermediate.write("root = ");
			while((instr = in1.readLine()) != null)
				outIntermediate.write(instr);
			
			outIntermediate.write("\n\n");
			while((instr = in2.readLine()) != null)
				outIntermediate.write(instr + "\n");
			
			outIntermediate.write("\n\n");
			while((instr = in3.readLine()) != null)
				outIntermediate.write(instr + "\n");
			
			System.out.println("closing 3 file readers and file writer");
			in1.close();
			in2.close();
			in3.close();
			outIntermediate.close();
			System.out.println("exiting try statement");
		}catch(Exception e){System.out.println("error combining three js text files, file possibly not found: " + e.getMessage());return;}
		
		// Process js file
		String shlArgs[] = {intermediate};
		
		System.out.println("about to call process....");
		// Create an instance of myself to call nonstatic functions
		process(shlArgs);
		try{
			File f = new File(intermediate);
			//File f2 = new File(jsonObjIn);
			boolean success = f.delete();
			//boolean success2 = f2.delete();

		    if (!success)// || !success2)
		      throw new IllegalArgumentException("Delete: deletion failed");
		}catch(Exception e){System.err.println(intermediate + " or " + jsonObjIn + " processing file does not exist: " + e.getMessage());}
	}
	
	/**
	 * processes the json file that contains the rules, processor, and json object
	 * @param args - an array that contains the name of the json file
	 */
	public void process(String[] args)
	{
		System.out.println("process function called");
		// Setup javascript functions that need to be translated to java
		String[] names = {  "print", "quit", "version", "load", "help" };
        this.defineFunctionProperties(names, RulesProcessor.class,
                                       ScriptableObject.DONTENUM);
        
        // Setup context...?
		Context cx = Context.enter();
		// Setup standard javascript objects
		Scriptable scope = cx.initStandardObjects(this);
		
		try{
			// Setup string buffer which will hold what to write to file when print is called
			toWrite = "";
			// Use rhino's process function to process the javascript file
			processSource(cx,args[0]);
		}catch(Exception e){System.err.println("RulesProcessor - process: " + e.getMessage());}
	}

	// Required to extend Shell class
	@Override
	public String getClassName() {
		// TODO Auto-generated method stub
		return null;
	}
	
	// Called whenever javascript print function is called
	public static void print(Context cx, Scriptable thisObj,
            Object[] args, Function funObj)
	{
		for (int i=0; i < args.length; i++) {
			//if (i > 0)
			//System.out.print(" ");
			
			// Convert the arbitrary JavaScript value into a string form.
			String s = Context.toString(args[i]);
			
			// Print what is going to be written
			//System.out.print(s);
			
			// Store what was printed in this variable which will be written to file
			toWrite += s;
		}
	}
	
	/**
	 * Runs the Server-Side javascript contained in the file "filename"; 
	 * treats the file like javascript in a shell
	 * 
	 * Outputs the result file (the final json file)
	 * note: processor.txt contains helper javascript functions
	 * @param cx - rhino thing
	 * @param filename - the final json file that contains rules.txt, processor.txt, and json object
	 * @throws IOException
	 */
	private void processSource(Context cx, String filename) throws IOException
    {
		System.out.println("Process Source function called");
		
		// create directories if necessary
		String outFileCopy = "";
		int index = 0;
		while(!outFileCopy.equals(outFile))
		{
			index = outFile.indexOf("/", index)+1;
			if(index == 0)
				break;
			outFileCopy = outFile.substring(0,index);
			File creation = new File(outFileCopy);
			if(!creation.exists())
				creation.mkdir();
		}
		File resultsFile = new File(outFile);
		outResults = new PrintWriter(new FileOutputStream(resultsFile));
		
		// setting up the results data structure
		if(jsFileType == JSFileType.PDFObj)
			outResults.write("{\n\"results\":[\n");
		
		// runs rhino in the shell
        if (filename == null) {
            BufferedReader in = new BufferedReader
                (new InputStreamReader(System.in));
            String sourceName = "<stdin>";
            int lineno = 1;
            boolean hitEOF = false;
            do {
                int startline = lineno;
                System.err.print("js> ");
                System.err.flush();
                try {
                    String source = "";
                    // Collect lines of source to compile.
                    while(true) {
                        String newline;
                        newline = in.readLine();
                        if (newline == null) {
                            hitEOF = true;
                            break;
                        }
                        source = source + newline + "\n";
                        lineno++;
                        // Continue collecting as long as more lines
                        // are needed to complete the current
                        // statement.  stringIsCompilableUnit is also
                        // true if the source statement will result in
                        // any error other than one that might be
                        // resolved by appending more source.
                        if (cx.stringIsCompilableUnit(source))
                            break;
                    }
                    Object result = cx.evaluateString(this, source,
                                                      sourceName, startline,
                                                      null);
                    
                    if (result != Context.getUndefinedValue()) {
                        System.err.println(Context.toString(result));
                    }
                }
                catch (WrappedException we) {
                    // Some form of exception was caught by JavaScript and
                    // propagated up.
                    System.err.println(we.getWrappedException().toString());
                    we.printStackTrace();
                }
                catch (EvaluatorException ee) {
                    // Some form of JavaScript error.
                    System.err.println("js: " + ee.getMessage());
                }
                catch (JavaScriptException jse) {
                    // Some form of JavaScript error.
                    System.err.println("js: " + jse.getMessage());
                }
                catch (IOException ioe) {
                    System.err.println(ioe.toString());
                }
                if (quitting) {
                    // The user executed the quit() function.
                    break;
                }
            } while (!hitEOF);
            System.err.println();
        }
        // runs rhino on a file
        else {
            FileReader in = null;
            try {
                in = new FileReader(filename);
            }
            catch (FileNotFoundException ex) {
                Context.reportError("Couldn't open file \"" + filename + "\".");
                return;
            }

            try {
                // Here we evalute the entire contents of the file as
                // a script. Text is printed only if the print() function
                // is called.
                cx.evaluateReader(this, in, filename, 1, null);
                
                // Write to file what is stored in write variable
                //if(toWrite != null)
                {
                	//out.write(toWrite);
                	//toWrite = null;
                }
            }
            catch (WrappedException we) {
                System.err.println(we.getWrappedException().toString());
                we.printStackTrace();
            }
            catch (EvaluatorException ee) {
                System.err.println("js: " + ee.getMessage());
            }
            catch (JavaScriptException jse) {
                System.err.println("js: " + jse.getMessage());
            }
            catch (IOException ioe) {
                System.err.println(ioe.toString());
            }
            finally {
                try {
                    in.close();
                }
                catch (IOException ioe) {
                    System.err.println(ioe.toString());
                }
            }
        }
        
        // remove the last comma in the results list
        if(jsFileType == JSFileType.PDFObj)
        {
        	int lastCommaInd = toWrite.lastIndexOf("},");
        	if(lastCommaInd >= 0)
        		toWrite = toWrite.substring(0, lastCommaInd) + "}\n";
        }
        
        // write what to file what is in the buffer
    	outResults.println(toWrite);
    	System.out.print("toWrite:");
    	System.out.println(toWrite);
    	// close the results object
        if(jsFileType == JSFileType.PDFObj)
        	outResults.println("]}");
        outResults.flush();
        outResults.close();
    }

	private boolean quitting;
	
	public void quit()
    {
        quitting = true;
    }
	
	public static double version(Context cx, Scriptable thisObj,
            Object[] args, Function funObj)
	{
		double result = cx.getLanguageVersion();
		if (args.length > 0) {
		double d = Context.toNumber(args[0]);
		cx.setLanguageVersion((int) d);
		}
		return result;
	}
		
	public static void load(Context cx, Scriptable thisObj,
		            Object[] args, Function funObj)
	{
		RulesProcessor shell = (RulesProcessor)getTopLevelScope(thisObj);
		for (int i = 0; i < args.length; i++) {
			try{
		shell.processSource(cx, Context.toString(args[i]));
			}catch(Exception e){System.err.println("RulesProcessor - load: " + e.getMessage());}
		}
	}
	
    public void help() {
        p("");
        p("Command                Description");
        p("=======                ===========");
        p("help()                 Display usage and help messages. ");
        p("defineClass(className) Define an extension using the Java class");
        p("                       named with the string argument. ");
        p("                       Uses ScriptableObject.defineClass(). ");
        p("load(['foo.js', ...])  Load JavaScript source files named by ");
        p("                       string arguments. ");
        p("loadClass(className)   Load a class named by a string argument.");
        p("                       The class must be a script compiled to a");
        p("                       class file. ");
        p("print([expr ...])      Evaluate and print expressions. ");
        p("quit()                 Quit the shell. ");
        p("version([number])      Get or set the JavaScript version number.");
        p("");
    }
    
    private static void p(String s) {
        System.out.println(s);
    }
	
}
