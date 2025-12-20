<Path>Components > DataGrid > TreeDataGrid</Path>

TreeDataGrid component is designed to display and sort tabular data, and provides means to display hierarchical data and manipulate rows and columns with greater performance due to lazy loading of data while scrolling. For TreeDataGrid, two attributes should be set: dataContainer which binds treeDataGrid to a data container, and hierarchyProperty which is the name of the entity attribute which references the same entity. The functionality of TreeDataGrid is similar to a simple DataGrid.

data-grid-tree.xml

<view xmlns="http://jmix.io/schema/flowui/view">
    <data>
        <collection id="tasksDc"
                    class="io.jmix.uisamples.entity.Task">
            <fetchPlan extends="_local">
                <property name="parentTask" fetchPlan="_local"/>
                <property name="assignee" fetchPlan="_local"/>
            </fetchPlan>
            <loader id="tasksDl">
                <query>
                    <![CDATA[select e from Task e]]>
                </query>
            </loader>
        </collection>
    </data>
    <facets>
        <dataLoadCoordinator auto="true"/>
    </facets>
    <layout>
        <select id="columnSelect" label="Hierarchy column"/>
        <treeDataGrid id="taskDataGrid"
                      dataContainer="tasksDc"
                      hierarchyProperty="parentTask"
                      width="100%"
                      minHeight="20em">
            <columns>
                <column property="name"/>
                <column property="dueDate"/>
                <column property="assignee"/>
            </columns>
        </treeDataGrid>
    </layout>
</view>




DataGridTreeSample.java

package io.jmix.uisamples.view.flowui.components.datagrid.tree;

import com.vaadin.flow.component.AbstractField.ComponentValueChangeEvent;
import com.vaadin.flow.component.grid.Grid;
import com.vaadin.flow.component.notification.Notification;
import com.vaadin.flow.component.select.Select;
import com.vaadin.flow.component.treegrid.CollapseEvent;
import com.vaadin.flow.component.treegrid.ExpandEvent;
import io.jmix.core.MessageTools;
import io.jmix.core.MetadataTools;
import io.jmix.core.metamodel.model.MetaPropertyPath;
import io.jmix.flowui.Notifications;
import io.jmix.flowui.component.grid.TreeDataGrid;
import io.jmix.flowui.component.select.JmixSelect;
import io.jmix.flowui.kit.component.ComponentUtils;
import io.jmix.flowui.view.*;
import io.jmix.uisamples.entity.Task;
import org.springframework.beans.factory.annotation.Autowired;

import java.util.Collection;
import java.util.LinkedHashMap;
import java.util.List;
import java.util.Map;
import java.util.stream.Collectors;

@ViewController("data-grid-tree")
@ViewDescriptor("data-grid-tree.xml")
public class DataGridTreeSample extends StandardView {

    @ViewComponent
    protected JmixSelect<String> columnSelect;
    @ViewComponent
    protected TreeDataGrid<Task> taskDataGrid;

    @Autowired
    protected MessageTools messageTools;
    @Autowired
    protected MetadataTools metadataTools;
    @Autowired
    protected Notifications notifications;

    @Subscribe
    protected void onInit(InitEvent event) {
        initColumnSelect();
    }

    @Subscribe("taskDataGrid")
    protected void onCollapse(CollapseEvent<Task, TreeDataGrid<Task>> event) {
        notifications.create("Collapsed Items: " + mapItemsToString(event.getItems()))
                .withPosition(Notification.Position.BOTTOM_END)
                .show();
    }

    @Subscribe("taskDataGrid")
    protected void onExpand(ExpandEvent<Task, TreeDataGrid<Task>> event) {
        notifications.create("Expanded Items: " + mapItemsToString(event.getItems()))
                .withPosition(Notification.Position.BOTTOM_END)
                .show();
    }

    protected void initColumnSelect() {
        ComponentUtils.setItemsMap(columnSelect, getColumnSelectItemsMap());
        columnSelect.setValue(taskDataGrid.getColumnByKey("name").getKey());
        columnSelect.addValueChangeListener(this::onColumnSelectValueChange);
    }

    protected void onColumnSelectValueChange(ComponentValueChangeEvent<Select<String>, String> event) {
        Grid.Column<Task> prevColumn = taskDataGrid.getColumnByKey(event.getOldValue());
        Grid.Column<Task> newColumn = taskDataGrid.getColumnByKey(event.getValue());

        int prevColumnIdx = taskDataGrid.getColumns().indexOf(prevColumn);
        int newColumnIdx = taskDataGrid.getColumns().indexOf(newColumn);

        MetaPropertyPath prevColumnMpp = taskDataGrid.getColumnMetaPropertyPath(prevColumn);
        MetaPropertyPath newColumnMpp = taskDataGrid.getColumnMetaPropertyPath(newColumn);

        taskDataGrid.removeColumn(prevColumn);
        taskDataGrid.setColumnPosition(taskDataGrid.addColumn(prevColumnMpp), prevColumnIdx);

        taskDataGrid.removeColumn(newColumn);
        taskDataGrid.setColumnPosition(taskDataGrid.addHierarchyColumn(newColumnMpp), newColumnIdx);
    }

    protected Map<String, String> getColumnSelectItemsMap() {
        List<Grid.Column<Task>> columns = taskDataGrid.getColumns();

        return columns.stream()
                .collect(Collectors.toMap(
                        Grid.Column::getKey,
                        this::columnMapper,
                        (oldValue, newValue) -> oldValue,
                        LinkedHashMap::new
                ));
    }

    protected String columnMapper(Grid.Column<Task> column) {
        MetaPropertyPath propertyPath = taskDataGrid.getColumnMetaPropertyPath(column);

        return propertyPath != null
                ? messageTools.getPropertyCaption(propertyPath.getMetaProperty())
                : column.getKey();
    }

    protected String mapItemsToString(Collection<Task> items) {
        return items.stream()
                .map(metadataTools::getInstanceName)
                .collect(Collectors.joining(", "));
    }
}




Task.java

package io.jmix.uisamples.entity;

import io.jmix.core.entity.annotation.JmixGeneratedValue;
import io.jmix.core.metamodel.annotation.InstanceName;
import io.jmix.core.metamodel.annotation.JmixEntity;
import jakarta.persistence.*;

import java.util.Date;
import java.util.UUID;

@Table(name = "TASK")
@Entity
@JmixEntity
public class Task {

    @Id
    @Column(name = "ID")
    @JmixGeneratedValue
    protected UUID id;

    @InstanceName
    @Column(name = "NAME", nullable = false)
    protected String name;

    @Temporal(TemporalType.TIMESTAMP)
    @Column(name = "DUE_DATE")
    protected Date dueDate;

    @ManyToOne(fetch = FetchType.LAZY)
    @JoinColumn(name = "ASSIGNEE_ID")
    protected Customer assignee;

    @ManyToOne(fetch = FetchType.LAZY)
    @JoinColumn(name = "PARENT_TASK_ID")
    protected Task parentTask;

    public Task() {
        this.id = UUID.randomUUID();
    }

    public UUID getId() {
        return id;
    }

    public void setId(UUID id) {
        this.id = id;
    }

    public void setParentTask(Task parentTask) {
        this.parentTask = parentTask;
    }

    public Task getParentTask() {
        return parentTask;
    }

    public void setName(String name) {
        this.name = name;
    }

    public String getName() {
        return name;
    }

    public void setDueDate(Date dueDate) {
        this.dueDate = dueDate;
    }

    public Date getDueDate() {
        return dueDate;
    }

    public void setAssignee(Customer assignee) {
        this.assignee = assignee;
    }

    public Customer getAssignee() {
        return assignee;
    }
}


