function hiddenAnswer() {
    // 获取页面中的所有table元素，这里假设只有一个目标table，如果有多个需要根据实际情况调整选择逻辑
    var tables = document.getElementsByTagName('table');
    for (var i = 0; i < tables.length; i++) {
        var table = tables[i];
        // 从第二行（索引为1，因为索引从0开始）开始遍历表格的行
        for (var j = 1; j < table.rows.length; j++) {
            var row = table.rows[j];
            // 去除第3 - 6列（索引为2 - 5）单元格的class属性
            for (var k = 2; k < 6; k++) {
                if (row.cells[k]) {
                    row.cells[k].removeAttribute('class');
                }
            }
            // 获取第7列（索引为6）的单元格
            var targetCell = row.cells[6];
            if (targetCell) {
                // 设置第7列单元格的初始背景颜色为黑色
                targetCell.style.backgroundColor = 'black';
                // 添加鼠标悬停（mouseover）事件监听器
                targetCell.addEventListener('mouseover', function () {
                    this.style.backgroundColor = 'white';
                });
                // 添加鼠标移出（mouseout）事件监听器
                targetCell.addEventListener('mouseout', function () {
                    this.style.backgroundColor = 'black';
                });
            }
        }
    }
}

window.onload = function () {
    var floatButton = document.getElementById('floatButton');
    if (floatButton) {
        floatButton.addEventListener('click', function () {
            hiddenAnswer();
            floatButton.style.display = 'none';
        });
    }
};



