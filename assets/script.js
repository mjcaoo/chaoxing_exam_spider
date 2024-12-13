// 创建按钮的函数
function createButton(text, id, classNames, clickHandler) {
  let button = document.createElement("button");
  button.textContent = text;
  if (id) {
    button.id = id;
  }
  if (classNames) {
    button.classList.add(classNames);
  }
  if (clickHandler) {
    button.addEventListener("click", clickHandler);
  }
  document.body.appendChild(button);
  return button;
}
// 隐藏答案
function hiddenAnswer() {
  var tables = document.getElementsByTagName("table");
  for (var i = 0; i < tables.length; i++) {
    var table = tables[i];
    // 从第二行（索引为1，因为索引从0开始）开始遍历表格的行
    for (var j = 1; j < table.rows.length; j++) {
      var row = table.rows[j];
      // 去除第3 - 6列（索引为2 - 5）单元格的class属性
      for (var k = 2; k < 6; k++) {
        if (row.cells[k]) {
          row.cells[k].removeAttribute("class");
        }
      }
      // 获取第7列（索引为6）的单元格
      var targetCell = row.cells[6];
      if (targetCell) {
        // 设置第7列单元格的初始背景颜色为黑色
        targetCell.style.backgroundColor = "black";
        // 添加鼠标悬停（mouseover）事件监听器
        targetCell.addEventListener("mouseover", function () {
          this.style.backgroundColor = "white";
        });
        // 添加鼠标移出（mouseout）事件监听器
        targetCell.addEventListener("mouseout", function () {
          this.style.backgroundColor = "black";
        });
      }
    }
  }
}
// 自测模式按钮点击事件
window.onload = function () {
  // 创建按钮
  const floatButton = createButton(
    "隐藏答案",
    "floatButton",
    "float-button",
    null
  );
  if (floatButton) {
    floatButton.addEventListener("click", function () {
      hiddenAnswer();
      floatButton.style.display = "none";
    });
  }
};
