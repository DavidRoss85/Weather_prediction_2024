from src.model.structures import Range

ranges = [Range(0,99),Range(200,299),Range(300,399)]
lst=[]

# for _ in range(len(ranges)):
#     lst.append([])
#
# for i,span in enumerate(ranges):
#     for n in range(span.low,span.high):
#         lst[i].append(n)
#         print(n)

def recursive(all_ranges:list,x:list=[]):
    ranges_copy=all_ranges.copy()
    current_range=ranges_copy.pop(0)

    for i in range(current_range.low,current_range.high+1):
        y=x.copy()
        y.append(i)
        if len(ranges_copy) > 0:
                recursive(ranges_copy,y)
        else:
            print(f"your array: {y}")


recursive(ranges,[])