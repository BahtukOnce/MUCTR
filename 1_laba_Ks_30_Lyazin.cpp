// ������� 4
// ��������� �������� ���������, ������� ����� ��������� ������ ������� ����� ��� ������ 
// ��������� ������ ����������. �������� ����� ��������� ��������� ������������� ������������������
// ����� � ������ �� ��� ���������� �� ��� ��� �� ������� �����. 
// �� �����, ����� ������� ������������������ ������� �����.

#include <iostream>

using namespace std;

void Add(int *array, int n);
void Eratosthene(int *array, int n);
void Print_Result(int *array, int n);


int main()
{	
	int n;
  	cout << "n  = ";
  	cin >> n;
  	n++;
  	int array[n];
  	
  	// ���������� �������.
  	Add(array, n);
  	
  	// ��������� ��������� �����.
  	Eratosthene(array, n);
    
    // �����.
	Print_Result(array, n);
	
  	return 0;
}


/*
 * ���������� ���������� ������
 *
 * @param ������ �� ������ ������.
 * @param n ������� ������ �����.
 *
 * �������� �������� �� 0 �� n � ��������� ���������� ������.
 */
 
void Add(int *array, int n)
{
	// ������������������ �� 0 �� n ������������.
  	for (int i = 0; i < n; i++)
    	array[i] = i;
}


/*
 * ������ ���������� (��������� ��������� �����)
 *
 * @param ������ �� ������ ������.
 * @param n ������� ������ �����.
 *
 * �������� �������� �� 2 �� n (���� i)
 * �������� �������� �� ���������� �������� i ����� ��� i (2 * i) � �������� ������ �������.
 * �������� �������� ������� (1 ������) ��� �� ����� �� ����������� � �������.
 */
 
void Eratosthene(int *array, int n)
{
	// ������� �� �������� 2, �������� ������ i �������, ������� �� ����������.
    for (int i = 2; i < n; i++)
    {
    	for (int j = 2 * i; j < n; j += i)
    	{
    		array[j] = 0;
		}
	}
	
	// ��������� ��������� �������.
	array[1] = 0;
}


/*
 * ����� ����������
 *
 * @param ������ �� ������ ������.
 * @param n ������� ������ �����.
 *
 * �������� �������� �� 0 �� n (���� i)
 * ������� ��� ��������� ��������
 */

void Print_Result(int *array, int n)
{
	for (int i = 0; i < n; i++)
	{
		if (array[i] != 0) cout << array[i] << endl;
	}
}
