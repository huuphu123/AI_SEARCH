# AI_BTL



WATER_SORT: Mỗi state là một list các string, mỗi string biểu diễn cho một bình nước, mỗi màu trong bình được mã hóa thành một kí tự. Kí tự đầu của mỗi string tương ứng với màu dưới bottom của bình ứng với string đó.

Hàm heuristic cho watersort: h(S) = c(S) + j(S) S:state - một list các cup. Trong đó: c(S) là tổng của các c(cup). Mỗi c(cup) được tính như sau: mỗi cup được phân rã thành các chuỗi con liên tiếp, mỗi chuỗi con chỉ gồm kí tự (màu) giống nhau. Khi đó c(cup) bằng số chuỗi con trừ đi 1. Ý nghĩa c(cup): giả sử cup 'XDDV' phân rã thành 'X', 'DD', 'V', thì khi đó cần tối thiều 2 bước để chuyển V, và DD qua cup khác.

j(S): lập một list A gồm màu dưới bottom của mỗi cup, cup nào rỗng thì ko tính. j(S) bằng số phần tử của A trừ đi số phần tử phân biệt của A. Ý nghĩa: giả sử có hai cup đều có chung màu bottom, thì khi đó cũng cần ít nhất một bước để xử lí đưa cột màu ở bottom cup này qua cốc kia. Nếu có 3 cup có cùng màu ở bottom thì cũng cần ít nhất 2 bước để xử lí ->quy nạp lên!!!!
