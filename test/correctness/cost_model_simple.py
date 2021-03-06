'''
Simple test case for checking get_cost
'''
import unittest
import cnn_mapping as cm 

class TestCostModel(unittest.TestCase):

    
    def test_simple(self):
        capacity_list = [512, 16384, 262144, 2097152]
        access_cost_list = [1, 6, 23, 64]
        static_cost_list = [0.2, 32*0.2, 512*0.2, 4096*0.2] 
        para_count_list = [4, 16]
        para_shared_level_list = [2, 4]

        loop_order_list = [(0, 2, 1, 1), (1, 3, 2, 2), (2, 0, 3, 3), (3, 1, 4, 4), (4, 4, 0, 5), (5, 5, 5, 0), (6, 6, 6, 6)]
        loop_blockings_list = [(3, 1, 1, 1), (3, 1, 1, 1), (1, 4, 1, 1), (1, 4, 1, 1), (1, 1, 32, 1), (1, 1, 1, 4), (1, 1, 1, 1)]
        loop_partitionings_list = [(1, 1, 1, 1), (1, 1, 1, 1), (1, 2, 1, 1,), (1, 2, 1, 1), (1, 1, 1, 1), (1, 1, 1, 16), (1, 1, 1, 1)]

        point = cm.MappingPoint(loop_order_list, loop_blockings_list, loop_partitionings_list)
        resource = cm.Resource(capacity_list, access_cost_list, static_cost_list, para_count_list, para_shared_level_list)
        layer = cm.Layer(64, 32, 8, 8, 3, 3, 1)
        cost = cm.cost_model.get_cost(resource, point, layer, True)
        real_cost = (6400*32 + 2048*64 + 18432*64) + (6400*32 + 2048*64+18432*1)*6 + (6400 + 2048*64 + 18432)*23 + (6400+2048+18432)*64
        self.assertEqual(cost, real_cost)

    def test_buffer_too_large(self):
        capacity_list = [512, 16384, 262144, 2097152]
        access_cost_list = [1, 6, 23, 64]
        static_cost_list = [0.2, 32*0.2, 512*0.2, 4096*0.2] 
        para_count_list = [4, 16]
        para_shared_level_list = [2, 4]

        loop_order_list = [(0, 2, 1, 1), (1, 3, 2, 2), (2, 0, 3, 3), (3, 1, 4, 4), (4, 4, 0, 5), (5, 5, 5, 0), (6, 6, 6, 6)]
        loop_blockings_list = [(3, 1, 1, 1), (3, 1, 1, 1), (1, 256, 1, 1), (1, 256, 1, 1), (1, 1, 128, 1), (1, 1, 1, 16), (1, 1, 1, 1)]
        loop_partitionings_list = [(1, 1, 1, 1), (1, 1, 1, 1), (1, 2, 1, 1,), (1, 2, 1, 1), (1, 1, 1, 1), (1, 1, 1, 16), (1, 1, 1, 1)]

        point = cm.MappingPoint(loop_order_list, loop_blockings_list, loop_partitionings_list)
        resource = cm.Resource(capacity_list, access_cost_list, static_cost_list, para_count_list, para_shared_level_list)
        layer = cm.Layer(256, 128, 512, 512, 3, 3, 1)
        cost = cm.cost_model.get_cost(resource, point, layer, True)
        real_cost = float("inf")
        self.assertEqual(cost, real_cost)

    def test_invalide_partition(self):
        capacity_list = [512, 16384, 262144, 2097152]
        access_cost_list = [1, 6, 23, 64]
        static_cost_list = [0.2, 32*0.2, 512*0.2, 4096*0.2] 
        para_count_list = [4, 16]
        para_shared_level_list = [2, 4]

        loop_order_list = [(0, 2, 1, 1), (1, 3, 2, 2), (2, 0, 3, 3), (3, 1, 4, 4), (4, 4, 0, 5), (5, 5, 5, 0), (6, 6, 6, 6)]
        loop_blockings_list = [(3, 1, 1, 1), (3, 1, 1, 1), (1, 128, 1, 1), (1, 256, 1, 1), (1, 1, 128, 1), (1, 1, 1, 16), (1, 1, 1, 1)]
        loop_partitionings_list = [(1, 1, 1, 1), (1, 1, 1, 1), (1, 4, 1, 1,), (1, 2, 1, 1), (1, 1, 1, 1), (1, 1, 1, 16), (1, 1, 1, 1)]

        point = cm.MappingPoint(loop_order_list, loop_blockings_list, loop_partitionings_list)
        resource = cm.Resource(capacity_list, access_cost_list, static_cost_list, para_count_list, para_shared_level_list)
        layer = cm.Layer(256, 128, 512, 512, 3, 3, 1)
        cost = cm.cost_model.get_cost(resource, point, layer, True)
        real_cost = float("inf")
        self.assertEqual(cost, real_cost)

    def test_invalide_parallelism(self):
        capacity_list = [512, 16384, 262144, 2097152]
        access_cost_list = [1, 6, 23, 64]
        static_cost_list = [0.2, 32*0.2, 512*0.2, 4096*0.2] 
        para_count_list = [4, 16]
        para_shared_level_list = [2, 3]

        loop_order_list = [(0, 2, 1, 1), (1, 3, 2, 2), (2, 0, 3, 3), (3, 1, 4, 4), (4, 4, 0, 5), (5, 5, 5, 0), (6, 6, 6, 6)]
        loop_blockings_list = [(3, 1, 1, 1), (3, 1, 1, 1), (1, 4, 1, 1), (1, 4, 1, 1), (1, 1, 32, 1), (1, 1, 1, 4), (1, 1, 1, 1)]
        loop_partitionings_list = [(1, 1, 1, 1), (1, 1, 1, 1), (1, 2, 1, 1,), (1, 2, 1, 1), (1, 1, 1, 1), (1, 1, 1, 16), (1, 1, 1, 1)]

        point = cm.MappingPoint(loop_order_list, loop_blockings_list, loop_partitionings_list)
        resource = cm.Resource(capacity_list, access_cost_list, static_cost_list, para_count_list, para_shared_level_list)
        layer = cm.Layer(64, 32, 8, 8, 3, 3, 1)
        cost = cm.cost_model.get_cost(resource, point, layer, True)
        real_cost = float("inf")
        self.assertEqual(cost, real_cost)


if __name__ == '__main__':
    unittest.main()
