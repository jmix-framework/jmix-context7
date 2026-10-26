<Path>Components > DataGrid > TreeDataGrid with hierarchy renderer</Path>

`HierarchyColumnComponentRenderer` displays custom components in a `TreeDataGrid` hierarchy column while preserving its expand and collapse control. This sample renders an icon next to each task name.


data-grid-tree-custom-renderer.xml

<view xmlns="http://jmix.io/schema/flowui/view">
    <data readOnly="true">
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




DataGridTreeCustomRendererSample.java

package io.jmix.uisamples.view.flowui.components.datagrid.treecustomrenderer;

import com.vaadin.flow.component.html.Span;
import com.vaadin.flow.component.icon.VaadinIcon;
import com.vaadin.flow.component.orderedlayout.HorizontalLayout;
import com.vaadin.flow.component.treegrid.HierarchyColumnComponentRenderer;
import com.vaadin.flow.data.renderer.Renderer;
import io.jmix.flowui.component.grid.TreeDataGrid;
import io.jmix.flowui.view.StandardView;
import io.jmix.flowui.view.Supply;
import io.jmix.flowui.view.ViewComponent;
import io.jmix.flowui.view.ViewController;
import io.jmix.flowui.view.ViewDescriptor;
import io.jmix.uisamples.entity.Task;

@ViewController("data-grid-tree-custom-renderer")
@ViewDescriptor("data-grid-tree-custom-renderer.xml")
public class DataGridTreeCustomRendererSample extends StandardView {

    @ViewComponent
    protected TreeDataGrid<Task> taskDataGrid;

    @Supply(to = "taskDataGrid.name", subject = "renderer")
    protected Renderer<Task> nameRenderer() {
        return new HierarchyColumnComponentRenderer<>(task -> {
            HorizontalLayout layout = new HorizontalLayout();
            layout.setPadding(false);
            layout.setAlignItems(HorizontalLayout.Alignment.CENTER);
            layout.add(VaadinIcon.BRIEFCASE.create(), new Span(task.getName()));

            return layout;
        }, taskDataGrid);
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


