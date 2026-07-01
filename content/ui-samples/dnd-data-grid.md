<Path>Cookbook > Drag and Drop > Drag and Drop for DataGrid</Path>

This sample demonstrates row drag-and-drop between two grids for the three grid types: `DataGrid`, `TreeDataGrid`, and `GroupDataGrid`.
Each tab shows two grids side-by-side, and a row can be dragged from one grid into the other.

Dragging is enabled with `rowsDraggable="true"`, and each grid is a drop target with `dropMode="ON_GRID"`. The `GridDragStartEvent` remembers the dragged rows and their source container, and the `GridDropEvent` listener moves them into the target container.

For the `TreeDataGrid`, the dragged node is moved together with its whole subtree and becomes a root node in the target tree. For the `GroupDataGrid`, the moved rows are regrouped automatically by the grouping column.


dnd-data-grid.xml

<view xmlns="http://jmix.io/schema/flowui/view"
      xmlns:groupg="http://jmix.io/schema/groupgrid/ui">
    <data>
        <collection id="customersSourceDc" class="io.jmix.uisamples.entity.Customer" fetchPlan="_base">
            <loader id="customersSourceDl">
                <query>
                    <![CDATA[select e from Customer e]]>
                </query>
            </loader>
        </collection>
        <collection id="customersTargetDc" class="io.jmix.uisamples.entity.Customer" fetchPlan="_base"/>

        <collection id="tasksSourceDc" class="io.jmix.uisamples.entity.Task">
            <fetchPlan extends="_local">
                <property name="parentTask" fetchPlan="_local"/>
                <property name="assignee" fetchPlan="_local"/>
            </fetchPlan>
            <loader id="tasksSourceDl">
                <query>
                    <![CDATA[select e from Task e]]>
                </query>
            </loader>
        </collection>
        <collection id="tasksTargetDc" class="io.jmix.uisamples.entity.Task">
            <fetchPlan extends="_local">
                <property name="parentTask" fetchPlan="_local"/>
                <property name="assignee" fetchPlan="_local"/>
            </fetchPlan>
        </collection>

        <collection id="customersGroupSourceDc" class="io.jmix.uisamples.entity.Customer" fetchPlan="_base">
            <loader id="customersGroupSourceDl">
                <query>
                    <![CDATA[select e from Customer e]]>
                </query>
            </loader>
        </collection>
        <collection id="customersGroupTargetDc" class="io.jmix.uisamples.entity.Customer" fetchPlan="_base"/>
    </data>
    <facets>
        <dataLoadCoordinator auto="true"/>
    </facets>
    <layout>
        <tabSheet width="100%" height="100%">
            <tab id="dataGridTab" label="DataGrid">
                <hbox width="100%" height="100%">
                    <dataGrid id="customersSourceGrid" dataContainer="customersSourceDc"
                              height="100%"
                              rowsDraggable="true" dropMode="ON_GRID" minHeight="20em">
                        <columns>
                            <column property="name"/>
                            <column property="lastName"/>
                            <column property="grade"/>
                        </columns>
                    </dataGrid>
                    <dataGrid id="customersTargetGrid" dataContainer="customersTargetDc"
                              height="100%"
                              rowsDraggable="true" dropMode="ON_GRID" minHeight="20em">
                        <columns>
                            <column property="name"/>
                            <column property="lastName"/>
                            <column property="grade"/>
                        </columns>
                    </dataGrid>
                </hbox>
            </tab>
            <tab id="treeDataGridTab" label="TreeDataGrid">
                <hbox width="100%" height="100%">
                    <treeDataGrid id="tasksSourceGrid" dataContainer="tasksSourceDc"
                                  hierarchyProperty="parentTask"
                                  height="100%"
                                  rowsDraggable="true" dropMode="ON_GRID" minHeight="20em">
                        <columns>
                            <column property="name"/>
                            <column property="assignee"/>
                        </columns>
                    </treeDataGrid>
                    <treeDataGrid id="tasksTargetGrid" dataContainer="tasksTargetDc"
                                  hierarchyProperty="parentTask"
                                  height="100%"
                                  rowsDraggable="true" dropMode="ON_GRID" minHeight="20em">
                        <columns>
                            <column property="name"/>
                            <column property="assignee"/>
                        </columns>
                    </treeDataGrid>
                </hbox>
            </tab>
            <tab id="groupDataGridTab" label="GroupDataGrid">
                <hbox width="100%" height="100%">
                    <groupg:groupDataGrid id="customersGroupSourceGrid" dataContainer="customersGroupSourceDc"
                                          height="100%"
                                          rowsDraggable="true" dropMode="ON_GRID" minHeight="20em">
                        <groupg:groupBy>
                            <groupg:columnRef key="grade"/>
                        </groupg:groupBy>
                        <groupg:columns>
                            <groupg:groupColumn header="Group"/>
                            <groupg:column property="grade"/>
                            <groupg:column property="name"/>
                            <groupg:column property="lastName"/>
                        </groupg:columns>
                    </groupg:groupDataGrid>
                    <groupg:groupDataGrid id="customersGroupTargetGrid" dataContainer="customersGroupTargetDc"
                                          height="100%"
                                          rowsDraggable="true" dropMode="ON_GRID" minHeight="20em">
                        <groupg:groupBy>
                            <groupg:columnRef key="grade"/>
                        </groupg:groupBy>
                        <groupg:columns>
                            <groupg:groupColumn header="Group"/>
                            <groupg:column property="grade"/>
                            <groupg:column property="name"/>
                            <groupg:column property="lastName"/>
                        </groupg:columns>
                    </groupg:groupDataGrid>
                </hbox>
            </tab>
        </tabSheet>
    </layout>
</view>




DndDataGridSample.java

package io.jmix.uisamples.view.flowui.cookbook.dragdrop.datagrid;

import com.vaadin.flow.component.grid.Grid;
import io.jmix.flowui.component.grid.DataGrid;
import io.jmix.flowui.component.grid.TreeDataGrid;
import io.jmix.flowui.component.groupgrid.GroupInfo;
import io.jmix.flowui.model.CollectionContainer;
import io.jmix.flowui.view.*;
import io.jmix.groupgridflowui.component.GroupDataGrid;
import io.jmix.uisamples.entity.Customer;
import io.jmix.uisamples.entity.Task;

import java.util.ArrayList;
import java.util.List;
import java.util.Set;
import java.util.stream.Collectors;

@ViewController("dnd-data-grid")
@ViewDescriptor("dnd-data-grid.xml")
public class DndDataGridSample extends StandardView {

    @ViewComponent
    private DataGrid<Customer> customersSourceGrid;
    @ViewComponent
    private DataGrid<Customer> customersTargetGrid;
    @ViewComponent
    private CollectionContainer<Customer> customersSourceDc;
    @ViewComponent
    private CollectionContainer<Customer> customersTargetDc;

    @ViewComponent
    private TreeDataGrid<Task> tasksSourceGrid;
    @ViewComponent
    private TreeDataGrid<Task> tasksTargetGrid;
    @ViewComponent
    private CollectionContainer<Task> tasksSourceDc;
    @ViewComponent
    private CollectionContainer<Task> tasksTargetDc;

    @ViewComponent
    private GroupDataGrid<Customer> customersGroupSourceGrid;
    @ViewComponent
    private GroupDataGrid<Customer> customersGroupTargetGrid;
    @ViewComponent
    private CollectionContainer<Customer> customersGroupSourceDc;
    @ViewComponent
    private CollectionContainer<Customer> customersGroupTargetDc;

    private List<?> draggedItems;
    private CollectionContainer<?> sourceDc;

    @Subscribe
    public void onInit(InitEvent event) {
        setupRowTransfer(customersSourceGrid, customersSourceDc, customersTargetGrid, customersTargetDc);

        setupSubtreeTransfer(tasksSourceGrid, tasksSourceDc, tasksTargetGrid, tasksTargetDc);

        setupGroupRowTransfer(customersGroupSourceGrid, customersGroupSourceDc,
                customersGroupTargetGrid, customersGroupTargetDc);
    }

    private void setupRowTransfer(Grid<?> gridA, CollectionContainer<?> dcA,
                                  Grid<?> gridB, CollectionContainer<?> dcB) {
        rememberDraggedItems(gridA, dcA);
        rememberDraggedItems(gridB, dcB);

        gridA.addDropListener(dropEvent -> moveRows(dcA));
        gridB.addDropListener(dropEvent -> moveRows(dcB));
    }

    private void setupSubtreeTransfer(TreeDataGrid<Task> gridA, CollectionContainer<Task> dcA,
                                      TreeDataGrid<Task> gridB, CollectionContainer<Task> dcB) {
        rememberDraggedItems(gridA, dcA);
        rememberDraggedItems(gridB, dcB);

        gridA.addDropListener(dropEvent -> moveSubtrees(dcA));
        gridB.addDropListener(dropEvent -> moveSubtrees(dcB));
    }

    private void rememberDraggedItems(Grid<?> grid, CollectionContainer<?> dc) {
        grid.addDragStartListener(dragStartEvent -> {
            draggedItems = dragStartEvent.getDraggedItems();
            sourceDc = dc;
        });
    }

    private void setupGroupRowTransfer(GroupDataGrid<Customer> gridA, CollectionContainer<Customer> dcA,
                                       GroupDataGrid<Customer> gridB, CollectionContainer<Customer> dcB) {
        gridA.setDragFilter(item -> dcA.getItems().contains(item));
        gridB.setDragFilter(item -> dcB.getItems().contains(item));

        rememberDraggedGroupRows(gridA, dcA);
        rememberDraggedGroupRows(gridB, dcB);

        gridA.addDropListener(dropEvent -> moveGroupRows(dcA, gridA, gridB));
        gridB.addDropListener(dropEvent -> moveGroupRows(dcB, gridA, gridB));
    }

    private void rememberDraggedGroupRows(GroupDataGrid<Customer> grid, CollectionContainer<Customer> dc) {
        grid.addDragStartListener(dragStartEvent -> {
            draggedItems = dragStartEvent.getDraggedItems();
            sourceDc = dc;
        });
    }

    private void moveGroupRows(CollectionContainer<Customer> targetDc,
                               GroupDataGrid<Customer> gridA, GroupDataGrid<Customer> gridB) {
        Set<GroupInfo> expandedA = expandedGroups(gridA);
        Set<GroupInfo> expandedB = expandedGroups(gridB);

        moveRows(targetDc);

        restoreExpandedGroups(gridA, expandedA);
        restoreExpandedGroups(gridB, expandedB);
    }

    private Set<GroupInfo> expandedGroups(GroupDataGrid<Customer> grid) {
        return grid.getRootGroups().stream()
                .filter(grid::isExpanded)
                .collect(Collectors.toSet());
    }

    private void restoreExpandedGroups(GroupDataGrid<Customer> grid, Set<GroupInfo> expandedGroups) {
        grid.getRootGroups().stream()
                .filter(expandedGroups::contains)
                .forEach(grid::expand);
    }

    @SuppressWarnings({"unchecked", "rawtypes"})
    private void moveRows(CollectionContainer targetDc) {
        if (draggedItems == null || sourceDc == null || sourceDc == targetDc) {
            return;
        }
        targetDc.getMutableItems().addAll(draggedItems);
        ((CollectionContainer) sourceDc).getMutableItems().removeAll(draggedItems);

        clearDragState();
    }

    @SuppressWarnings("unchecked")
    private void moveSubtrees(CollectionContainer<Task> targetDc) {
        if (draggedItems == null || sourceDc == null || sourceDc == targetDc) {
            return;
        }

        CollectionContainer<Task> from = (CollectionContainer<Task>) sourceDc;
        for (Object item : draggedItems) {
            Task root = (Task) item;
            List<Task> subtree = new ArrayList<>();

            collectSubtree(root, from, subtree);
            root.setParentTask(null);

            targetDc.getMutableItems().addAll(subtree);
            from.getMutableItems().removeAll(subtree);
        }

        clearDragState();
    }

    private void collectSubtree(Task root, CollectionContainer<Task> dc, List<Task> result) {
        result.add(root);
        for (Task task : dc.getItems()) {
            if (root.equals(task.getParentTask())) {
                collectSubtree(task, dc, result);
            }
        }
    }

    private void clearDragState() {
        draggedItems = null;
        sourceDc = null;
    }
}


