
# chap2 陣列&結構

## 2.1 array0
### 2.1.1 抽象化資料結構
Array由<index,value>組成
### 2.1.2 C language 下的陣列
- link list 的陣列
	- `int *list;`
	- 透過指標直接指向記憶體空間
	- 配合malloc食用
- 一般固定大小陣列
	- `int list[5];`
	- `int list[]={1,2,3,4,5,6,7,8,9,10}`
## 2.2 動態陣列
### 2.2.1 一維陣列
```
int main() {
    // 使用malloc
    int *arr = (int *)malloc(5 * sizeof(int));
    free(new_arr);
    return 0;
}
```
### 2.2.2 二維陣列
![](https://th.bing.com/th/id/R.550976ea4de76c6e83a297d5699ae843?rik=4D851ZSDlc5q%2bQ&riu=http%3a%2f%2f3.bp.blogspot.com%2f-_-Izz3tAT9w%2fVQ1jX7dwU2I%2fAAAAAAAAAG8%2fba9KC3ERA30%2fs1600%2fdynamics_2d_array.png&ehk=gKTgu05j9EcWHhHGTGYZaR%2brIz3DSU%2fpivQMoE7CxOk%3d&risl=&pid=ImgRaw&r=0)
#### malloc (分配記憶體)
`addr=(type *) malloc(length*siezof(type))`
#### realloc (重新分配記憶體，用於增加記憶體長度)
`new_addr=(type *) realloc(old_addr,new_length*siezof(type))`

## 2.3 結構(struct)&連結(link list)
### 2.3.1 結構(struct)
- `typedef struct`
	```
	typedef struct{
		char name[10];
		int age;
		float salary;
	}example_use;
	int main(int k,char *arr[]){
		example_use asd;
		asd.age =0;
		printf("%d\n",asd.age); 
		return 0;
	}
	```
- `struct`
	```
	struct example_2{
		char name[10];
		int age;
		float salary;
	};
	int main(int k,char *arr[]){
		struct example_2 as2;
		as2.salary=1.234;
		printf("%f",as2.salary); 
		return 0;
	}
	```
### 2.3.2 union
```
#include <stdio.h>

union SampleUnion {
    int intValue;
    float floatValue;
    char stringValue[20];
};

int main() {
    union SampleUnion myUnion;

    myUnion.intValue = 42;
    printf("Integer value: %d\n", myUnion.intValue);

    myUnion.floatValue = 3.14;
    printf("Float value: %f\n", myUnion.floatValue);

    strcpy(myUnion.stringValue, "Hello, Union!");
    printf("String value: %s\n", myUnion.stringValue);

    return 0;
}

```
### 2.3.3 結構內部實作
簡單而言，不用我們擔心
### 2.3.4 自我參考表(常見於link list)
```
struct link{
	int value;	
	struct link* next;
};

```
## 2.4 多項式
### 2.4.1 抽象化資料型態
懶得做xN，簡單而言就是可以用在很多地方
### 2.4.2 多項式表示方式
```
struct poly{
	int degree;//最高級數
	float coef[100];//每級的係數
};
```

```
struct poly add(struct poly A,struct poly B){
	struct poly D;
	if (A.degree<B.degree){
		D.degree=B.degree;
	}else{
		D.degree=A.degree;
	}
	int i;
	for (i=0;i<D.degree;i++){
		D.coef[i]=A.coef[i]+B.coef[i];
	}
	
}
```

## 2.5 稀疏矩陣
### 2.5.1 抽象化資料型態
稀疏矩陣（英語：sparse matrix），在數值分析中，是其元素大部分為零的矩陣。反之，如果大部分元素都非零，則這個矩陣是稠密(dense)的。在科學與工程領域中求解線性模型時經常出現大型的稀疏矩陣。
### 2.5.2 稀疏矩陣表示方式
```
struct term{
	int col;
	int row;
	int value;
};
struct term matrix[item+1];
```
通常，在這個表示法的第一行，也就是matrix[0]會用於放置整個矩陣的基本訊息。
- matrix[0].col
	- matrix的行數
- matrix[0].row
	- matrix的列數
- matrix[0].value
	- matrix中的非0值的數量
- 排序
	- 升序
	- row>col

| i     | 0   | 1   | 2   | 3   | 4   | 5   | 6   | 7   | 8   |
| ----- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| r     | 6   | 0   | 0   | 0   | 1   | 1   | 2   | 4   | 5   |
| c     | 6   | 0   | 3   | 5   | 1   | 2   | 3   | 0   | 2   |
| value | 8   | 15  | 22  | -15 | 11  | 3   | -6  | 91  | 28  |

### 2.5.3 轉置矩陣
#### transpose
```
struct term *transpose(const struct term *A) {
    struct term *B = (struct term *)malloc(
			(A[0].value + 1) * sizeof(struct term));
    B[0].value = A[0].value;
    B[0].row = A[0].col;  
    B[0].col = A[0].row;
    if (A[0].value > 0) {
        int i, j, k;
        k = 1;
        for (i = 0; i < A[0].col; i++) {
            for (j = 1; j < A[0].value + 1; j++) {
                if (A[j].col == i) {
                    B[k].value = A[j].value;
                    B[k].col = A[j].row;
                    B[k].row = A[j].col;
                    k++;
                }
            }
        }
    }
    return B;
}
```
分析:
正常而言 bigO: $\mathcal{O}(col\times value)$
假設 value = $col\times row$
⇒ $\mathcal{O}(col^2 \times row)$
⇒ 太爛了
$$\frac{1}{2}$$
---

#### fast transport(use counting sort)
```
#define MAX_TERMS 101
#define MAX_COL 10

typedef struct {
	int row;
    int col;
    int value;
} Term;

void fastTranspose(Term a[], Term b[]) {
    int rowTerms[MAX_COL], startingPos[MAX_COL];

    int numCols = a[0].col;
    int numTerms = a[0].value;

    b[0].row = numCols;
    b[0].col = a[0].row;
    b[0].value = numTerms;

    if (numTerms > 0) {
    	int i;
        for ( i = 0; i < numCols; i++) {
            rowTerms[i] = 0;
        }

        for ( i = 1; i <= numTerms; i++) {
            rowTerms[a[i].col]++;
        }

        startingPos[0] = 1;

        for ( i = 1; i < numCols; i++) {
            startingPos[i] = startingPos[i - 1] + rowTerms[i - 1];
        }

        for ( i = 1; i <= numTerms; i++) {
            int j = startingPos[a[i].col]++;
            b[j].row = a[i].col;
            b[j].col = a[i].row;
            b[j].value = a[i].value;
        }
    }
}
```
基本上就跟counting sort 的內容非常相像
### 2.5.4 矩陣乘法
```
#define MAX_TERMS 100
typedef struct {
    int row;
    int col;
    int value;
} Term;
void sparseMatrixMultiplication(Term A[], Term B[], Term result[]) {
    // Initialize result matrix
    for (int i = 0; i < MAX_TERMS; ++i) {
        result[i].row = 0;
        result[i].col = 0;
        result[i].value = 0;
    }

    // Multiply matrices A and B
    for (int i = 0; i < MAX_TERMS && A[i].value != 0; ++i) {
        for (int j = 0; j < MAX_TERMS && B[j].value != 0; ++j) {
            if (A[i].col == B[j].row) {
                // Multiply and accumulate
                result[i].value += A[i].value * B[j].value;
                result[i].row = A[i].row;
                result[i].col = B[j].col;
            }
        }
    }
}
```