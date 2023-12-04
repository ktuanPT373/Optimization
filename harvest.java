import java.io.PrintWriter;
import java.util.Random;
import java.util.Scanner;

public class TSP {
    int n;// number of points (cities)
    int[][] c;// c[i,j] is the travel distance from i to j
    int[] x;// solution representation;
    boolean[] visited;
    int f;// distance accumulated
    int fmin;// distance of the best solution found so far
    int Cmin;// shortest segment of the distance matrix c
    void loadData(){
        try{
            Scanner in = new Scanner(System.in);
            n = in.nextInt();
            c = new int[n+1][];
            for(int i = 1; i <= n; i++)
                c[i] = new int[n+1];

            for(int i = 1; i <= n; i++)
                for(int j = 1; j <= n; j++)
                    c[i][j] = in.nextInt();
            Cmin = 100000000;
            for(int i = 1;i <= n; i++)
                for(int j = 1; j <= n; j++)
                    if(i != j && Cmin > c[i][j]) Cmin = c[i][j];

        }catch (Exception e){
            e.printStackTrace();
        }
    }
    void genData(String filename, int n, int M){
        try{
            Random R = new Random();
            PrintWriter out = new PrintWriter(filename);
            out.println(n);
            for(int i = 1; i <= n; i++){
                for(int j = 1; j <= n; j++){
                    int c = R.nextInt()%M + 1;
                    if(i == j) c = 0;
                    if(c < 0) c = -c;
                    out.print(c + " ");
                }
                out.println();
            }
            out.close();
        }catch (Exception e){
            e.printStackTrace();
        }

    }
    void solution(){
        int D = f + c[x[n]][x[1]];
        //System.out.print("Current solution: ");
        //for(int i = 1; i <= n; i++) System.out.print(x[i] + " ");
        //System.out.println(x[1] + ", distance = " + D);
        if(D < fmin){
            fmin = D;// the current solution is better than the best found so far
            System.out.println("Update best " + fmin);
        }
    }
    void Try(int k){
        for(int v = 1; v <= n; v++){
            if(visited[v] == false){
                x[k] = v;
                visited[v] = true;
                f = f + c[x[k-1]][x[k]];

                if(k == n) solution();
                else{
                
                    int g = f + Cmin*(n-k+1);// lower bound of the distance of the
                            // complete solution developed from current point x[k]
                    //if(g < fmin)  // branch and bound
                        Try(k+1);

                }
                visited[v] = false;
                f = f - c[x[k-1]][x[k]];
            }
        }
    }
    void solve(){
        loadData();
        x = new int[n+1];// uses indices from 1, 2, .., n
        visited = new boolean[n+1];
        x[1] = 1;// FIX the starting point 1
        visited[1] = true;
        f = 0;
        fmin = 1000000000;
        Try(2);
        System.out.println("shortest tour is " + fmin);
    }
    public static void main(String[] args){
        double t0 = System.currentTimeMillis();
        TSP app = new TSP();
        app.solve();
        double t = System.currentTimeMillis() - t0;
        System.out.println("time = " + (t*0.001) + " seconds");
        //app.genData("tsp-15.txt",15,20);
    }
}
