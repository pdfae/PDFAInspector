import org.mozilla.javascript.*;
import org.mozilla.javascript.optimizer.*;
import java.io.*;

import com.itextpdf.*;
public class Test extends Shell{

	/**
	 * @param args
	 */
	public static void main(String[] args) {
		// TODO Auto-generated method stub
		/*try{
		BufferedReader in = new BufferedReader(new FileReader("files/ExampleJS.txt"));
		
		}catch(Exception e){System.err.println("Test main: " + e.getMessage());}*/
		
		String shlArgs[] = {"files/ExampleJS.txt"};
		/*
		Shell shl = new Shell();
		System.out.println("judging...");
		shl.main(shlArgs);
		System.out.println("finished!");
		*/
		
		Test t = new Test();
		t.process();
		
		String[] argz = {"print(\"yo!\")"};
		//shell.main(argz);
		
		RunScript test2 = new RunScript();
		//test2.main(scc);
		
	}
	
	public void process()
	{
		String[] names = { "print", "quit", "version", "load", "help" };
        this.defineFunctionProperties(names, Test.class,
                                       ScriptableObject.DONTENUM);
        
		Context cx = Context.enter();
		Shell shell = new Shell();
		Scriptable scope = cx.initStandardObjects(shell);
		//cx.evaluateString(scope, "print(\"yo!\");", "eh", 1, null);
		String[] argz = {};
		processSource(cx,null);
		
		Object result = cx.evaluateString(this, "document.write(\"yo!\");", "eh", 1, null);
		System.out.println(result.toString());
		
	}

	@Override
	public String getClassName() {
		// TODO Auto-generated method stub
		return null;
	}
	
	public static void print(Context cx, Scriptable thisObj,
            Object[] args, Function funObj)
	{
		for (int i=0; i < args.length; i++) {
		if (i > 0)
		System.out.print(" ");
		
		// Convert the arbitrary JavaScript value into a string form.
		String s = Context.toString(args[i]);
		
		System.out.print(s);
		System.out.print("yes!");
		}
		System.out.println();
	}
	
	private void processSource(Context cx, String filename)
    {
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
		Shell shell = (Shell)getTopLevelScope(thisObj);
		for (int i = 0; i < args.length; i++) {
		shell.processSource(cx, Context.toString(args[i]));
	}
}
	
}
