class DurationSum(object):
    def __init__(self,arr):
        if type(arr) != list:
            raise TypeError("DurationSum constructor expects list(int)")
        for x in arr:
            if type(x) != int:
                raise TypeError("DurationSum constructor expects list(int)")
            if x <= 0:
                raise ValueError("DurationSum constructor expects an array of positive integers")
        self._base = arr
        t = 0
        self._total = []
        for x in arr:
            self._total.append(t)
            t += x
    def get(self,index):
        return self._base[index]
    def forward(self,index):
        return self._total[index]
    def backward(self,value):
        index_low = 0
        index_high = len(self._total) - 1
        while index_high - index_low > 1:
            index_med = (index_low + index_high) // 2
            s = self._total[index_med]
            if s > value:
                index_high = index_med
                continue
            if s < value:
                index_low = index_med
                continue
            # s == value
            return index_med, 0
        s = self._total[index_high]
        if value >= s:
            return index_high, value-s
        s = self._total[index_low]
        return index_low, value-s