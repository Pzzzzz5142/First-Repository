from NetWork import Network
import os
import struct

class Loader(object):
    def __init__(self, path, count):
        '''
        初始化加载器
        path: 数据文件路径
        count: 文件中的样本个数
        '''
        self.path = path
        self.count = count

    def get_file_content(self):
        '''
        读取文件内容
        '''
        f = open(self.path, 'rb')
        content = f.read()
        '''
        tmp=[]
        tt=bytes()
        cnt=0
        for i in range(len(content)//8):
            tmp.append(content[i*8:i*8+8])
        content=tmp
        '''
        
        f.close()
        return content

    def to_int(self, byte):
        '''
        将unsigned byte字符转换为整数
        '''
        return byte
        #return struct.unpack('B', byte)[0]

class ImageLoader(Loader):
    def get_picture(self, content, index):
        '''
        内部函数，从文件中获取图像
        '''
        start = index * 28 * 28 + 16
        picture = []
        for i in range(28):
            picture.append([])
            for j in range(28):
                picture[i].append(
                    self.to_int(content[start + i * 28 + j]))
        return picture

    def get_one_sample(self, picture):
        '''
        内部函数，将图像转化为样本的输入向量
        '''
        sample = []
        for i in range(28):
            for j in range(28):
                sample.append(picture[i][j])
        return sample

    def load(self):
        '''
        加载数据文件，获得全部样本的输入向量
        '''
        content = self.get_file_content()
        data_set = []
        for index in range(self.count):
            data_set.append(
                self.get_one_sample(
                    self.get_picture(content, index)))
        return data_set

# 标签数据加载器
class LabelLoader(Loader):
    def load(self):
        '''
        加载数据文件，获得全部样本的标签向量
        '''
        content = self.get_file_content()
        labels = []
        for index in range(self.count):
            labels.append(self.norm(content[index + 8]))
        return labels

    def norm(self, label):
        '''
        内部函数，将一个值转换为10维标签向量
        '''
        label_vec = []
        label_value = self.to_int(label)
        for i in range(10):
            if i == label_value:
                label_vec.append(0.9)
            else:
                label_vec.append(0.1)
        return label_vec


def get_training_data_set():
    '''
    获得训练数据集
    '''
    image_loader = ImageLoader('./LML/MyNetWork/train-images.idx3-ubyte', 60000)
    label_loader = LabelLoader('./LML/MyNetWork/train-labels.idx1-ubyte', 60000)
    return image_loader.load(), label_loader.load()


def get_test_data_set():
    '''
    获得测试数据集
    '''
    image_loader = ImageLoader('./LML/MyNetWork/t10k-images.idx3-ubyte', 10000)
    label_loader = LabelLoader('./LML/MyNetWork/t10k-labels.idx1-ubyte', 10000)
    return image_loader.load(), label_loader.load()

def get_result(vec):
    max_value_index = 0
    max_value = 0
    for i in range(len(vec)):
        if vec[i] > max_value:
            max_value = vec[i]
            max_value_index = i
    return max_value_index

def evaluate(network, test_data_set, test_labels):
    error = 0
    total = len(test_data_set)

    for i in range(total):
        label = get_result(test_labels[i])
        predict = get_result(network.predict(test_data_set[i]))
        if label != predict:
            error += 1
    return float(error) / float(total)

if __name__ == "__main__":
    net=Network(784)
    data,label = get_training_data_set()
    test_data_set, test_labels = get_test_data_set()
    print('爷读完了')
    net.add_layer(512)
    #net.add_layer(512)
    net.add_layer(10)
    print('爷初始化完了')
    net.train(data,label,0.1,10)
    print(evaluate(net,test_data_set,test_labels))