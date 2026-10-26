<Path>Components > DataGrid > TreeDataGrid filtering that keeps parent rows</Path>

When the tree is filtered, each matching task is shown under its parent tasks, even if the parents don't match the filter. For example, the default filter finds `Task4`, and the tree shows it under `Task1` and `Task3`. `SimplePagination` counts only the matching tasks.

Without this solution, if the filter excludes a parent, `TreeDataGrid` hides its matching children, while `SimplePagination` still counts them.

How it works:

- `genericFilter` and `simplePagination` are bound to the `tasksDl` loader, so the `tasksDc` container holds only the matching tasks of the current page.
- The tree shows the `tasksTreeDc` container. When `tasksDc` changes, the `TreeAncestorsLoader` bean adds the missing parents loaded from the database, and the tree expands all rows.
- The tree container uses the standard sorter bound to `tasksDl`, so sorting by a column applies to all pages.

`showOrphans="true"` shows a task at the root level if its parent can't be loaded, for example, because of access restrictions. If you don't need to show the parents, this attribute alone is enough.


data-grid-tree-filter.xml

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
                    <![CDATA[select e from Task e order by e.name]]>
                </query>
            </loader>
        </collection>
        <collection id="tasksTreeDc"
                    class="io.jmix.uisamples.entity.Task"/>
    </data>
    <facets>
        <dataLoadCoordinator auto="true"/>
    </facets>
    <layout>
        <genericFilter id="genericFilter" dataLoader="tasksDl">
            <properties include=".*"/>
            <configurations>
                <configuration id="defaultConfiguration" name="Task name" default="true">
                    <propertyFilter property="name" operation="CONTAINS"
                                    operationEditable="true" defaultValue="Task4"/>
                </configuration>
            </configurations>
        </genericFilter>
        <simplePagination id="simplePagination"
                          itemsPerPageDefaultValue="4"
                          dataLoader="tasksDl"/>
        <treeDataGrid id="tasksDataGrid"
                      dataContainer="tasksTreeDc"
                      hierarchyProperty="parentTask"
                      showOrphans="true"
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




DataGridTreeFilterSample.java

package io.jmix.uisamples.view.flowui.components.datagrid.treefilter;

import io.jmix.flowui.component.grid.TreeDataGrid;
import io.jmix.flowui.model.CollectionContainer;
import io.jmix.flowui.model.CollectionContainerSortManager;
import io.jmix.flowui.model.CollectionLoader;
import io.jmix.flowui.view.*;
import io.jmix.uisamples.entity.Task;
import org.springframework.beans.factory.annotation.Autowired;

@ViewController("data-grid-tree-filter")
@ViewDescriptor("data-grid-tree-filter.xml")
public class DataGridTreeFilterSample extends StandardView {

    @ViewComponent
    private CollectionContainer<Task> tasksDc;
    @ViewComponent
    private CollectionLoader<Task> tasksDl;
    @ViewComponent
    private CollectionContainer<Task> tasksTreeDc;
    @ViewComponent
    private TreeDataGrid<Task> tasksDataGrid;

    @Autowired
    private TreeAncestorsLoader treeAncestorsLoader;
    @Autowired
    private CollectionContainerSortManager collectionContainerSortManager;

    @Subscribe
    public void onInit(InitEvent event) {
        tasksTreeDc.setSorter(collectionContainerSortManager.createCollectionContainerSorter(tasksTreeDc, tasksDl));
    }

    @Subscribe(id = "tasksDc", target = Target.DATA_CONTAINER)
    public void onTasksDcCollectionChange(CollectionContainer.CollectionChangeEvent<Task> event) {
        tasksTreeDc.setItems(treeAncestorsLoader.withAncestors(tasksDc, Task::getParentTask));
        tasksDataGrid.expand(tasksTreeDc.getItems());
    }
}




TreeAncestorsLoader.java

package io.jmix.uisamples.view.flowui.components.datagrid.treefilter;

import io.jmix.core.DataManager;
import io.jmix.core.FetchPlan;
import io.jmix.core.Id;
import io.jmix.core.LoadContext;
import io.jmix.flowui.model.CollectionContainer;
import org.springframework.stereotype.Component;

import java.util.*;
import java.util.function.Function;

/**
 * Completes the items of a container with their ancestors that are not in the container,
 * so that a tree can show every item under its parents.
 */
@Component
public class TreeAncestorsLoader {

    private final DataManager dataManager;

    public TreeAncestorsLoader(DataManager dataManager) {
        this.dataManager = dataManager;
    }

    /**
     * Returns the container items together with their missing ancestors. The ancestors are loaded
     * with the container fetch plan and placed right before the first item that needs them.
     *
     * @param container      container with the items to show in a tree
     * @param parentProvider function that returns the parent of an item or {@code null} for a root item
     * @param <E>            entity type
     * @return items with their ancestors
     */
    public <E> List<E> withAncestors(CollectionContainer<E> container, Function<E, E> parentProvider) {
        List<E> items = container.getItems();
        Map<Id<E>, E> ancestors = loadMissingAncestors(container, parentProvider);

        Set<Id<E>> addedIds = new HashSet<>();
        for (E item : items) {
            addedIds.add(Id.of(item));
        }

        List<E> result = new ArrayList<>(items.size() + ancestors.size());
        for (E item : items) {
            Deque<E> missingParents = new ArrayDeque<>();
            E parent = parentProvider.apply(item);

            while (parent != null
                    && ancestors.containsKey(Id.of(parent))
                    && addedIds.add(Id.of(parent))) {
                E ancestor = ancestors.get(Id.of(parent));
                missingParents.addFirst(ancestor);
                parent = parentProvider.apply(ancestor);
            }

            result.addAll(missingParents);
            result.add(item);
        }

        return result;
    }

    protected <E> Map<Id<E>, E> loadMissingAncestors(CollectionContainer<E> container,
                                                     Function<E, E> parentProvider) {
        Set<Id<E>> knownIds = new HashSet<>();
        for (E item : container.getItems()) {
            knownIds.add(Id.of(item));
        }

        Map<Id<E>, E> ancestors = new HashMap<>();
        Set<Id<E>> missingIds = getMissingParentIds(container.getItems(), parentProvider, knownIds);
        while (!missingIds.isEmpty()) {
            knownIds.addAll(missingIds);

            List<E> parents = loadByIds(container, missingIds);
            for (E parent : parents) {
                ancestors.put(Id.of(parent), parent);
            }

            missingIds = getMissingParentIds(parents, parentProvider, knownIds);
        }

        return ancestors;
    }

    private <E> Set<Id<E>> getMissingParentIds(Collection<E> entities,
                                               Function<E, E> parentProvider,
                                               Set<Id<E>> knownIds) {
        Set<Id<E>> parentIds = new HashSet<>();
        for (E entity : entities) {
            E parent = parentProvider.apply(entity);

            if (parent != null && !knownIds.contains(Id.of(parent))) {
                parentIds.add(Id.of(parent));
            }
        }

        return parentIds;
    }

    private <E> List<E> loadByIds(CollectionContainer<E> container, Collection<Id<E>> ids) {
        List<Object> idList = ids.stream()
                .map(Id::getValue)
                .toList();

        LoadContext<E> loadContext = new LoadContext<E>(container.getEntityMetaClass())
                .setIds(idList);

        FetchPlan fetchPlan = container.getFetchPlan();
        if (fetchPlan != null) {
            loadContext.setFetchPlan(fetchPlan);
        }

        return dataManager.loadList(loadContext);
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


