# python-api-testing
基于 python 语言实现接口自动化测试。

## unittest 

1. BeautifulReport.zip 解压后放入 python 安装目录 Lib\site-packages 中
2. 测试报告使用 BeautifulReport
3. html 报告中 用例描述 使用 excel 文件中的 title 列显示用例标题
4. ddt 默认使用测试用例的文档注释作为用例描述，可以通过修改 ddt 源代码的方式实现 3 中
    ```python
    # 将 ddt 源代码按照如下修改
    # test_data_docstring = _get_test_data_docstring(func, v)
    test_data_docstring = v["title"]
    ```

## pytest

1. 修改 allure 源码，使得不显示参数化的参数，从而使标题显示正常
```python
    # \Lib\site-packages\allure_pytest\listener.py
        test_result.parameters.extend(
            [Parameter(name=name, value=represent(value)) for name, value in params.items()])

    # 将上述源码修改为如下
    
        test_result.parameters.extend([])
```
