<Path>Add-ons > Kanban > Kanban with column actions</Path>

The Kanban board component supports changing column settings dynamically. To control this feature, use the collapsible, columnReorderingAllowed and columnActionsEnabled attributes. The collapsible attribute adds buttons for collapsing and expanding columns to the header. Collapsing is also available by double-clicking on the header. The columnReorderingAllowed attribute allows changing the order of columns using Drag'n'Drop. The columnActionsEnabled attribute adds a button that opens a dialog menu that allows you to hide, expand and collapse columns. The corresponding actions are available in the component's Java API. All the settings described above are saved in the view settings for the current user if SettingsFacet is added. When the view is reopened, the settings are applied again. The user's view settings save the order of columns and their state (visibility and collapsed state).

kanban-column-actions.xml

<view xmlns="http://jmix.io/schema/flowui/view"
      xmlns:kanban="http://jmix.io/schema/kanban/ui">
    <data readOnly="true">
        <collection id="kanbanTasksDc" class="io.jmix.uisamples.entity.KanbanTask">
            <fetchPlan extends="_base"/>
            <loader id="kanbanTasksDl" readOnly="true">
                <query>
                    <![CDATA[select e from KanbanTask e order by e.name asc]]>
                </query>
            </loader>
        </collection>
    </data>
    <facets>
        <dataLoadCoordinator auto="true"/>
        <settings auto="true"/>
    </facets>
    <layout>
        <hbox classNames="buttons-panel">
            <button id="collapseAllBtn" text="msg://collapseAllBtn.text" icon="COMPRESS"/>
            <button id="expandAllBtn" text="msg://expandAllBtn.text" icon="EXPAND"/>
            <button id="hideAllBtn" text="msg://hideAllBtn.text" icon="CIRCLE_THIN"/>
            <button id="showAllBtn" text="msg://showAllBtn.text" icon="CIRCLE"/>
        </hbox>
        <kanban:kanban id="kanban" dataContainer="kanbanTasksDc"
                       width="100%"
                       height="100%"
                       collapsible="true"
                       columnReorderingAllowed="true"
                       columnActionsEnabled="true"
                       taskTagsVisible="true">
            <kanban:propertiesMapping id="id"
                                      status="status"
                                      text="name"
                                      color="color"
                                      tags="tags"/>
            <kanban:columns>
                <kanban:column dataField="todo" label="msg://kanban.column.todo"/>
                <kanban:column dataField="in_progress" label="msg://kanban.column.in_progress"/>
                <kanban:column dataField="testing" label="msg://kanban.column.testing"/>
                <kanban:column dataField="done" label="msg://kanban.column.done"/>
            </kanban:columns>
        </kanban:kanban>
    </layout>
</view>




KanbanColumnActionsSample.java

package io.jmix.uisamples.view.flowui.kanban.columnactions;

import com.vaadin.flow.component.ClickEvent;
import io.jmix.flowui.kit.component.button.JmixButton;
import io.jmix.flowui.view.*;
import io.jmix.kanbanflowui.component.Kanban;
import io.jmix.uisamples.entity.KanbanTask;

@ViewController("kanban-column-actions")
@ViewDescriptor("kanban-column-actions.xml")
public class KanbanColumnActionsSample extends StandardView {

    @ViewComponent
    private Kanban<KanbanTask> kanban;

    @Subscribe("collapseAllBtn")
    public void onCollapseAllBtnClick(final ClickEvent<JmixButton> event) {
        kanban.getColumns().forEach(kanbanColumn -> {
            if (!kanbanColumn.isCollapsed() && kanbanColumn.isCollapsible()) {
                kanbanColumn.setCollapsed(true);
            }
        });
    }

    @Subscribe("expandAllBtn")
    public void onExpandAllBtnClick(final ClickEvent<JmixButton> event) {
        kanban.expandAllColumns();
    }

    @Subscribe("hideAllBtn")
    public void onHideAllBtnClick(final ClickEvent<JmixButton> event) {
        kanban.getColumns().forEach(kanbanColumn -> {
            if (kanbanColumn.isVisible()) {
                kanbanColumn.setVisible(false);
            }
        });
    }

    @Subscribe("showAllBtn")
    public void onShowAllBtnClick(final ClickEvent<JmixButton> event) {
        kanban.showAllColumns();
    }
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
import org.springframework.lang.Nullable;

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
import org.springframework.lang.Nullable;

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


