<Path>Components > DataGrid > TreeDataGrid with lazy nodes</Path>

This sample contains an example of implementing lazy data loading for TreeDataGrid. TaskLazyTreeDataGridItems is a data provider that is defined in the view controller. This provider loads data from the database using DataManager bean. When a hierarchy node is expanded, the required data is loaded from the database.

data-grid-tree-lazy-nodes.xml

<view xmlns="http://jmix.io/schema/flowui/view">
    <layout>
        <treeDataGrid id="taskDataGrid"
                      metaClass="Task"
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




DataGridTreeLazyNodesSample.java

package io.jmix.uisamples.view.flowui.components.datagrid.treelazynodes;

import com.vaadin.flow.component.notification.Notification;
import com.vaadin.flow.component.notification.NotificationVariant;
import com.vaadin.flow.data.provider.AbstractDataProvider;
import com.vaadin.flow.data.provider.hierarchy.HierarchicalDataProvider;
import com.vaadin.flow.data.provider.hierarchy.HierarchicalQuery;
import com.vaadin.flow.shared.Registration;
import io.jmix.core.*;
import io.jmix.core.entity.EntityValues;
import io.jmix.core.metamodel.model.MetaClass;
import io.jmix.core.metamodel.model.MetaPropertyPath;
import io.jmix.flowui.Notifications;
import io.jmix.flowui.component.grid.TreeDataGrid;
import io.jmix.flowui.data.BindingState;
import io.jmix.flowui.data.grid.DataGridItems;
import io.jmix.flowui.kit.event.EventBus;
import io.jmix.flowui.view.*;
import io.jmix.uisamples.entity.Task;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.lang.Nullable;

import java.util.ArrayList;
import java.util.Collection;
import java.util.List;
import java.util.function.Consumer;
import java.util.stream.Stream;

@ViewController("data-grid-tree-lazy-nodes")
@ViewDescriptor("data-grid-tree-lazy-nodes.xml")
public class DataGridTreeLazyNodesSample extends StandardView {

    @ViewComponent
    protected TreeDataGrid<Task> taskDataGrid;

    @Autowired
    protected Metadata metadata;
    @Autowired
    protected DataManager dataManager;
    @Autowired
    protected Notifications notifications;

    @Subscribe
    public void onInit(InitEvent event) {
        taskDataGrid.setDataProvider(new TaskLazyTreeDataGridItems());
    }

    public class TaskLazyTreeDataGridItems extends AbstractDataProvider<Task, Void>
            implements HierarchicalDataProvider<Task, Void>, DataGridItems.Sortable<Task> {

        private Task selectedItem;
        private Sort sort = Sort.UNSORTED;

        private EventBus eventBus;

        public TaskLazyTreeDataGridItems() {
        }

        @Override
        public int getChildCount(HierarchicalQuery<Task, Void> query) {
            return Math.toIntExact(getItems(query).size());
        }

        @Override
        public Stream<Task> fetchChildren(HierarchicalQuery<Task, Void> query) {
            Collection<Task> list = getItems(query);

            notifications.create(String.format("Loaded: %d items", list.size()))
                    .withPosition(Notification.Position.TOP_CENTER)
                    .withThemeVariant(NotificationVariant.LUMO_SUCCESS)
                    .show();

            return list.stream();
        }

        protected Collection<Task> getItems(HierarchicalQuery<Task, Void> query) {
            return dataManager.load(Task.class)
                    .query("select e from Task e where e.parentTask = :parent")
                    .parameter("parent", query.getParent())
                    .sort(sort)
                    .firstResult(query.getOffset())
                    .maxResults(query.getLimit())
                    .list();
        }

        @Override
        public Collection<Task> getItems() {
            return dataManager.load(Task.class)
                    .all()
                    .sort(sort)
                    .list();
        }

        @Nullable
        @Override
        public Task getItem(@Nullable Object itemId) {
            return itemId == null
                    ? null
                    : dataManager.load(Id.of(itemId, Task.class)).one();
        }

        @Override
        public Object getItemValue(Object itemId, MetaPropertyPath propertyId) {
            return EntityValues.getValueEx(getItem(itemId), propertyId);
        }

        @Override
        public Task getSelectedItem() {
            return selectedItem;
        }

        @Override
        public void setSelectedItem(Task item) {
            this.selectedItem = item;

            getEventBus().fireEvent(new SelectedItemChangeEvent<>(this, item));
        }

        @Override
        public void sort(Object[] propertyId, boolean[] ascending) {
            sort = createSort(propertyId, ascending);
        }

        @Override
        public void resetSortOrder() {
            sort = Sort.UNSORTED;
        }

        private Sort createSort(Object[] propertyId, boolean[] ascending) {
            List<Sort.Order> orders = new ArrayList<>();

            for (int i = 0; i < propertyId.length; i++) {
                String property;
                if (propertyId[i] instanceof MetaPropertyPath) {
                    property = ((MetaPropertyPath) propertyId[i]).toPathString();
                } else {
                    property = (String) propertyId[i];
                }

                Sort.Order order = ascending[i]
                        ? Sort.Order.asc(property)
                        : Sort.Order.desc(property);

                orders.add(order);
            }
            return Sort.by(orders);
        }

        @Override
        public boolean hasChildren(Task item) {
            LoadContext<Object> loadContext = new LoadContext<>(getEntityMetaClass())
                    .setQuery(new LoadContext.Query("select e from Task e where e.parentTask = :parent")
                            .setParameter("parent", item));

            return dataManager.getCount(loadContext) > 0;
        }

        public MetaClass getEntityMetaClass() {
            return metadata.getClass(Task.class);
        }

        @Override
        public Registration addStateChangeListener(Consumer<StateChangeEvent> listener) {
            return getEventBus().addListener(StateChangeEvent.class, listener);
        }

        @SuppressWarnings({"unchecked", "rawtypes"})
        @Override
        public Registration addValueChangeListener(Consumer<ValueChangeEvent<Task>> listener) {
            return getEventBus().addListener(ValueChangeEvent.class, ((Consumer) listener));
        }

        @SuppressWarnings({"unchecked", "rawtypes"})
        @Override
        public Registration addItemSetChangeListener(Consumer<ItemSetChangeEvent<Task>> listener) {
            return getEventBus().addListener(ItemSetChangeEvent.class, ((Consumer) listener));
        }

        @SuppressWarnings({"unchecked", "rawtypes"})
        @Override
        public Registration addSelectedItemChangeListener(Consumer<SelectedItemChangeEvent<Task>> listener) {
            return getEventBus().addListener(SelectedItemChangeEvent.class, ((Consumer) listener));
        }

        @Override
        public boolean containsItem(Task item) {
            return true;
        }

        @Override
        public boolean isInMemory() {
            return true;
        }

        @Override
        public Class<Task> getType() {
            return getEntityMetaClass().getJavaClass();
        }

        @Override
        public BindingState getState() {
            return BindingState.ACTIVE;
        }

        protected EventBus getEventBus() {
            if (eventBus == null) {
                eventBus = new EventBus();
            }

            return eventBus;
        }
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


