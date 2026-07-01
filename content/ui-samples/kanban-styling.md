<Path>Add-ons > Kanban > Kanban styling</Path>

There are different ways to style the Kanban board component. You can use component properties, renderers, and CSS classes to style it. Note that in this example, the color attribute is defined for the columns. Colors will be applied to the headers. Also, if you define the applyColumnColorToTasks attribute, the column color will be applied to the task card style. If the task has its own color, the task color will take precedence over the column color.

kanban-styling.xml

<view xmlns="http://jmix.io/schema/flowui/view"
      xmlns:kanban="http://jmix.io/schema/kanban/ui">
    <data>
        <collection id="kanbanTasksDc" class="io.jmix.uisamples.entity.KanbanTask">
            <fetchPlan extends="_base"/>
            <loader id="kanbanTasksDl">
                <query>
                    <![CDATA[select e from KanbanTask e order by e.name asc]]>
                </query>
            </loader>
        </collection>
    </data>
    <facets>
        <dataLoadCoordinator auto="true"/>
    </facets>
    <layout>
        <hbox width="100%" wrap="true">
            <button id="createBtn" action="kanban.create"/>
            <button id="editBtn" action="kanban.edit"/>
            <button id="removeBtn" action="kanban.remove"/>
        </hbox>
        <kanban:kanban id="kanban" dataContainer="kanbanTasksDc"
                       width="100%" height="100%"
                       columnColorEntireSurfaceEnabled="true"
                       applyColumnColorToTasks="true"
                       columnSummaryEnabled="true"
                       dropPlaceholderAllowed="true"
                       taskProgressVisible="true"
                       columnFooterVisible="true">
            <kanban:propertiesMapping id="id"
                                      status="status"
                                      text="name"
                                      progress="progress"
                                      tags="tags"
                                      color="color"/>

            <kanban:actions>
                <kanban:action id="create" type="list_create">
                    <kanban:properties>
                        <kanban:property name="openMode" value="DIALOG"/>
                    </kanban:properties>
                </kanban:action>
                <kanban:action id="edit" type="list_edit">
                    <kanban:properties>
                        <kanban:property name="openMode" value="DIALOG"/>
                    </kanban:properties>
                </kanban:action>
                <kanban:action id="remove" type="list_remove"/>
            </kanban:actions>

            <kanban:columns>
                <kanban:column dataField="todo" color="#006AF5"
                               label="msg://kanban.column.todo"/>
                <kanban:column dataField="in_progress" color="#CA150C"
                               label="msg://kanban.column.in_progress"/>
                <kanban:column dataField="testing" color="#FFCC00"
                               label="msg://kanban.column.testing"/>
                <kanban:column dataField="done" color="#192434"
                               label="msg://kanban.column.done"/>
            </kanban:columns>
        </kanban:kanban>
    </layout>
</view>




KanbanStylingSample.java

package io.jmix.uisamples.view.flowui.kanban.styling;

import io.jmix.flowui.view.StandardView;
import io.jmix.flowui.view.ViewController;
import io.jmix.flowui.view.ViewDescriptor;

@ViewController("kanban-styling")
@ViewDescriptor("kanban-styling.xml")
public class KanbanStylingSample extends StandardView {
}




KanbanTask.java

package io.jmix.uisamples.entity;

import io.jmix.core.entity.annotation.JmixGeneratedValue;
import io.jmix.core.metamodel.annotation.InstanceName;
import io.jmix.core.metamodel.annotation.JmixEntity;
import jakarta.persistence.*;
import jakarta.validation.constraints.Max;
import jakarta.validation.constraints.Min;
import jakarta.validation.constraints.NotNull;
import org.jspecify.annotations.Nullable;

import java.time.LocalDate;
import java.util.UUID;

@Table(name = "KANBAN_TASK", indexes = {
        @Index(name = "IDX_KANBAN_TASK_ASSIGNEE", columnList = "ASSIGNEE_ID")
})
@Entity
@JmixEntity
public class KanbanTask {

    @JmixGeneratedValue
    @Column(name = "ID", nullable = false)
    @Id
    private UUID id;

    @InstanceName
    @Column(name = "NAME", nullable = false)
    @NotNull
    private String name;

    @Column(name = "STATUS", nullable = false)
    @NotNull
    private String status;

    @ManyToOne(fetch = FetchType.LAZY)
    @JoinColumn(name = "ASSIGNEE_ID")
    private KanbanUser assignee;

    @Column(name = "COLOR")
    private String color;

    @Max(100)
    @Min(0)
    @Column(name = "PROGRESS")
    private Integer progress;

    @Column(name = "PRIORITY")
    private String priority;

    @Column(name = "DUE_DATE")
    private LocalDate dueDate;

    @Column(name = "TAGS")
    private String tags;

    public Integer getProgress() {
        return progress;
    }

    public void setProgress(Integer progress) {
        this.progress = progress;
    }

    @Nullable
    public String getColor() {
        return color;
    }

    public void setColor(String color) {
        this.color = color;
    }

    public KanbanUser getAssignee() {
        return assignee;
    }

    public void setAssignee(KanbanUser assignee) {
        this.assignee = assignee;
    }

    @Nullable
    public TaskPriority getPriority() {
        return priority == null ? null : TaskPriority.fromId(priority);
    }

    public void setPriority(@Nullable TaskPriority priority) {
        this.priority = priority == null ? null : priority.getId();
    }

    public void setTags(String tags) {
        this.tags = tags;
    }

    @Nullable
    public String getTags() {
        return tags;
    }

    public LocalDate getDueDate() {
        return dueDate;
    }

    public void setDueDate(LocalDate dueDate) {
        this.dueDate = dueDate;
    }

    public String getName() {
        return name;
    }

    public void setName(String name) {
        this.name = name;
    }

    @Nullable
    public TaskStatus getStatus() {
        return status == null ? null : TaskStatus.fromId(status);
    }

    public void setStatus(TaskStatus status) {
        this.status = status.getId();
    }

    public UUID getId() {
        return id;
    }

    public void setId(UUID id) {
        this.id = id;
    }
}




TaskStatus.java

package io.jmix.uisamples.entity;

import io.jmix.core.metamodel.datatype.EnumClass;
import org.jspecify.annotations.Nullable;

public enum TaskStatus implements EnumClass<String> {

    TODO("todo"),
    IN_PROGRESS("in_progress"),
    TESTING("testing"),
    TESTING_MANUAL("manual"),
    TESTING_AUTO("auto"),
    DONE("done");

    private final String id;

    TaskStatus(String id) {
        this.id = id;
    }

    @Override
    public String getId() {
        return id;
    }

    @Nullable
    public static TaskStatus fromId(String id) {
        for (TaskStatus at : TaskStatus.values()) {
            if (at.getId().equals(id)) {
                return at;
            }
        }
        return null;
    }
}


