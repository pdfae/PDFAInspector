import org.mozilla.javascript.*;
import org.mozilla.javascript.optimizer.*;
import java.io.*;

import com.itextpdf.*;
public class RulesProcessor extends Shell{

	/**
	 * @param args
	 */
	static String outFile = "files/testOut.txt";
	static BufferedWriter out;
	static String toWrite;
	public static void main(String[] args) {
		// TODO Auto-generated method stub
		/*try{
		BufferedReader in = new BufferedReader(new FileReader("files/ExampleJS.txt"));
		
		}catch(Exception e){System.err.println("Test main: " + e.getMessage());}*/
		
		String shlArgs[] = {"files/ExampleJS.txt"};
		//Shell shl = new Shell();
		System.out.println("judging...");
		//Context cx = new Context();
		//cx.enter();
		//shl.main(shlArgs);
		
		RulesProcessor processor = new RulesProcessor();
		processor.process(shlArgs);
		System.out.println("finished!");
	}
	
	public void process(String[] args)
	{
		String[] names = {  "print", "quit", "version", "load", "help" };
        this.defineFunctionProperties(names, RulesProcessor.class,
                                       ScriptableObject.DONTENUM);
        
		Context cx = Context.enter();
		Scriptable scope = cx.initStandardObjects(this);
		String[] argz = {};
		
		try{
			toWrite = "";
			processSource(cx,args[0]);
		}catch(Exception e){System.err.println("RulesProcessor - process: " + e.getMessage());}
	}

	@Override
	public String getClassName() {
		// TODO Auto-generated method stub
		return null;
	}
	
	public static void print(Context cx, Scriptable thisObj,
            Object[] args, Function funObj)
	{
		try{
			for (int i=0; i < args.length; i++) {
				if (i > 0)
				System.out.print(" ");
				
				// Convert the arbitrary JavaScript value into a string form.
				String s = Context.toString(args[i]);
				
				System.out.print(s);
				toWrite += s + "\n";
				
				System.out.println();
			}
		}catch(Exception e){System.err.println("RulesProcessor - print: " + e.getMessage());}
	}
	
	private void processSource(Context cx, String filename) throws IOException
    {
		BufferedWriter out = new BufferedWriter(new FileWriter(outFile));
		
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
                    
                    if(toWrite != "")
                    {
                    	out.write(toWrite);
                    	toWrite = "";
                    }
                    
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
        } else {
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
                
                if(toWrite != null)
                {
                	out.write(toWrite);
                	toWrite = null;
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
        out.close();
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
