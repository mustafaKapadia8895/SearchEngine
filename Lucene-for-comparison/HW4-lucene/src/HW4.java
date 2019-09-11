import java.io.BufferedReader;
import java.io.File;
//import java.io.FileOutputStream;
//import java.io.FileReader;
import java.io.IOException;
import java.io.InputStreamReader;
//import java.io.PrintStream;
//import java.util.ArrayList;

import org.apache.lucene.analysis.Analyzer;
import org.apache.lucene.analysis.core.SimpleAnalyzer;
//import org.apache.lucene.analysis.standard.StandardAnalyzer;
import org.apache.lucene.document.Document;
//import org.apache.lucene.document.Field;
//import org.apache.lucene.document.StringField;
//import org.apache.lucene.document.TextField;
import org.apache.lucene.index.DirectoryReader;
import org.apache.lucene.index.IndexReader;
//import org.apache.lucene.index.IndexWriter;
//import org.apache.lucene.index.IndexWriterConfig;
import org.apache.lucene.index.Term;
import org.apache.lucene.queryparser.classic.QueryParser;
import org.apache.lucene.search.IndexSearcher;
import org.apache.lucene.search.Query;
import org.apache.lucene.search.ScoreDoc;
import org.apache.lucene.search.TopDocs;
//import org.apache.lucene.search.TopScoreDocCollector;
import org.apache.lucene.store.FSDirectory;
import org.apache.lucene.util.Version;

/**
 * To create Apache Lucene index in a folder and add files into this index based
 * on the input of the user.
 */
public class HW4 {
    private static Analyzer analyzer = new SimpleAnalyzer(Version.LUCENE_47);
   // private static Analyzer sAnalyzer = new SimpleAnalyzer(Version.LUCENE_47);

    //private IndexWriter writer;
    //private ArrayList<File> queue = new ArrayList<File>();

    public static void main(String[] args) throws IOException {
	System.out
		.println("Enter the FULL path where the index will be created: (e.g. /Usr/index or c:\\temp\\index)");
    	
	String indexLocation = null;
	BufferedReader br = new BufferedReader(new InputStreamReader(System.in));
	String s =br.readLine();

	HW3 indexer = null;
	try {
	    indexLocation = s;
	    indexer = new HW3(s);
	} catch (Exception ex) {
	    System.out.println("Cannot create index..." + ex.getMessage());
	    System.exit(-1);
	}

	// ===================================================
	// read input from user until he enters q for quit
	// ===================================================
	int x=0;
	while (x!=1) {
	    try {
		System.out
			.println("Enter the FULL path to add into the index (q=quit): (e.g. /home/mydir/docs or c:\\Users\\mydir\\docs)");
		System.out
			.println("[Acceptable file types: .xml, .html, .html, .txt]");
		s = br.readLine();
		if (s.equalsIgnoreCase("q")) {
		    break;
		}

		// try to add file into the index
		indexer.indexFileOrDirectory(s);
	    } catch (Exception e) {
		System.out.println("Error indexing " + s + " : "
			+ e.getMessage());
	    }
	    x++;
	}

	// ===================================================
	// after adding, we always have to call the
	// closeIndex, otherwise the index is not created
	// ===================================================
	indexer.closeIndex();

	// =========================================================
	// Now search
	// =========================================================
	IndexReader reader = DirectoryReader.open(FSDirectory.open(new File(
		indexLocation)));
	IndexSearcher searcher = new IndexSearcher(reader);
	//TopScoreDocCollector collector = TopScoreDocCollector.create(100, true);
	//PrintStream out = new PrintStream(new FileOutputStream("output.txt"));
	

	s = "";
	while (!s.equalsIgnoreCase("q")) {
	    try {
		System.out.println("Enter the search query (q=quit):");
		s = br.readLine();
		if (s.equalsIgnoreCase("q")) {
		    break;
		}

		Query q = new QueryParser(Version.LUCENE_47, "contents",
			analyzer).parse(s);
		TopDocs docs = searcher.search(q, 100);
		ScoreDoc[] hits = docs.scoreDocs;
		

		// 4. display results
		System.out.println("Found " + hits.length + " hits.");
		for (int i = 0; i < hits.length; ++i) {
		    int docId = hits[i].doc;
		    Document d = searcher.doc(docId);
		    System.out.println((i + 1) + ". " + d.get("path")
			    + " score=" + hits[i].score);
		}
		// 5. term stats --> watch out for which "version" of the term
		// must be checked here instead!
		Term termInstance = new Term(s, "contents");
		long termFreq = reader.totalTermFreq(termInstance);
		long docCount = reader.docFreq(termInstance);
		System.out.println(s + " Term Frequency " + termFreq
			+ " - Document Frequency " + docCount);

	    } catch (Exception e) {
		System.out.println("Error searching " + s + " : "
			+ e.getMessage());
		break;
	    }

	}

    }
    

}

