<Path>Cookbook > Data in UI > Saving entity by custom service</Path>


This example demonstrates how to isolate entities when sending them from a view to a custom service. For additional information, see the [Working with Entities in UI]({docsBaseUrl}flow-ui/data/entities-in-ui.html) documentation section.

The list and detail views in this example allow users to manage the `Contract` entity which has a `status` enumeration attribute with the `DRAFT`, `APPROVED`, `REJECTED` possible values. 

The **Approve**, **Revise**, and **Reject** buttons in the detail view invoke the `ContractService` bean passing the edited `Contract` and a new status to it. The service updates the status in the entity instance and saves the changes.

The standard saving process of the view initiated by the **Save** button is intercepted by the `saveDelegate()` handler method. It also invokes the `ContractService` bean. Notice that the handler is called only if the entity has been modified since the last save.

Implementation details:

- [contract-detail-view.xml]({currentPath}?tab=contract-detail-view.xml)
  - `saveAction` is of the `detail_save` type. It does not close the view after clicking **Save**.
- [ContractDetailView.java]({currentPath}?tab=ContractDetailView.java)
  - `changeContractStatus()` method creates a copy of the edited entity and sends that copy to the service. The returned instance is merged into `DataContext`. The merged instance is ignored because it's used only by the view logic internally.
  - `saveDelegate()` handler is called by `DataContext` when the user clicks **Save**. It also creates a copy of the edited entity and sends it to the service for saving. The saved instance is returned from the service and the handler. It is merged by the `DataContext` implementation after exiting the handler.
- [ContractService.java]({currentPath}?tab=ContractService.java)
  - `changeStatus()` method updates the status of the entity instance and sends it to the `DataManager`. The updated instance is then returned to refresh the view state. If an exception occurs in the service method, the state of the entity presented in the view remains untouched, because the service operates with a copy of the entity.
- [ContractListView.java]({currentPath}?tab=ContractListView.java) defines "after close" handlers for `createAction` and `editAction` to always refresh the entities list after closing the detail view. This is required because data might be modified by the detail view while it was open.

Contract.java

package io.jmix.uisamples.entity;

import io.jmix.core.entity.annotation.JmixGeneratedValue;
import io.jmix.core.metamodel.annotation.InstanceName;
import io.jmix.core.metamodel.annotation.JmixEntity;
import jakarta.persistence.*;

import java.time.LocalDate;
import java.util.UUID;

@JmixEntity
@Table(name = "CONTRACT", indexes = {
        @Index(name = "IDX_CONTRACT_CUSTOMER", columnList = "CUSTOMER_ID")
})
@Entity
public class Contract {
    @JmixGeneratedValue
    @Column(name = "ID", nullable = false)
    @Id
    private UUID id;

    @Column(name = "VERSION", nullable = false)
    @Version
    private Integer version;

    @Column(name = "DATE_")
    private LocalDate date;

    @Column(name = "NUMBER_")
    private String number;

    @InstanceName
    @Column(name = "DESCRIPTION")
    private String description;

    @JoinColumn(name = "CUSTOMER_ID")
    @ManyToOne(fetch = FetchType.LAZY)
    private Customer customer;

    @Column(name = "STATUS", length = 1)
    private String status;

    @Column(name = "COMMENTS")
    @Lob
    private String comments;

    public String getComments() {
        return comments;
    }

    public void setComments(String comments) {
        this.comments = comments;
    }

    public ContractStatus getStatus() {
        return status == null ? null : ContractStatus.fromId(status);
    }

    public void setStatus(ContractStatus status) {
        this.status = status == null ? null : status.getId();
    }

    public Customer getCustomer() {
        return customer;
    }

    public void setCustomer(Customer customer) {
        this.customer = customer;
    }

    public String getNumber() {
        return number;
    }

    public void setNumber(String number) {
        this.number = number;
    }

    public String getDescription() {
        return description;
    }

    public void setDescription(String description) {
        this.description = description;
    }

    public LocalDate getDate() {
        return date;
    }

    public void setDate(LocalDate date) {
        this.date = date;
    }

    public Integer getVersion() {
        return version;
    }

    public void setVersion(Integer version) {
        this.version = version;
    }

    public UUID getId() {
        return id;
    }

    public void setId(UUID id) {
        this.id = id;
    }

}



contract-detail-view.xml

<?xml version="1.0" encoding="UTF-8" standalone="no"?>
<view xmlns="http://jmix.io/schema/flowui/view"
      title="msg://contractDetailView.title"
      focusComponent="form">
    <data>
        <instance id="contractDc"
                  class="io.jmix.uisamples.entity.Contract">
            <fetchPlan extends="_base">
                <property name="customer" fetchPlan="_base"/>
            </fetchPlan>
            <loader id="contractDl"/>
        </instance>
    </data>
    <facets>
        <dataLoadCoordinator auto="true"/>
    </facets>
    <actions>
        <action id="saveAction" type="detail_save" actionVariant="DEFAULT"/>
        <action id="closeAction" type="detail_close"/>
    </actions>
    <layout>
        <formLayout id="form" dataContainer="contractDc">
            <responsiveSteps>
                <responsiveStep minWidth="0" columns="1"/>
                <responsiveStep minWidth="40em" columns="2"/>
            </responsiveSteps>
            <textField property="status" readOnly="true"/>
            <datePicker id="dateField" property="date"/>
            <textField id="numberField" property="number"/>
            <entityPicker id="customerField" property="customer">
                <actions>
                    <action id="entityLookupAction" type="entity_lookup"/>
                    <action id="entityClearAction" type="entity_clear"/>
                </actions>
            </entityPicker>
            <textField id="descriptionField" property="description"/>
            <textArea id="commentsField" height="9.5em" property="comments"/>
        </formLayout>
        <hbox id="detailActions">
            <button id="approveButton" text="msg://approve"/>
            <button id="reviseButton" text="msg://revise"/>
            <button id="rejectButton" text="msg://reject"/>
            <button id="saveAndCloseButton" action="saveAction" text="msg:///actions.Save"/>
            <button id="closeButton" action="closeAction" text="msg:///actions.Close"/>
        </hbox>
    </layout>
</view>




ContractDetailView.java

package io.jmix.uisamples.view.flowui.cookbook.customservice1;

import com.vaadin.flow.component.ClickEvent;
import com.vaadin.flow.component.notification.Notification;
import com.vaadin.flow.router.Route;
import io.jmix.core.Copier;
import io.jmix.core.SaveContext;
import io.jmix.flowui.Notifications;
import io.jmix.flowui.kit.component.button.JmixButton;
import io.jmix.flowui.model.DataContext;
import io.jmix.flowui.model.InstanceContainer;
import io.jmix.flowui.view.*;
import io.jmix.uisamples.entity.Contract;
import io.jmix.uisamples.entity.ContractStatus;
import io.jmix.uisamples.view.sys.main.MainView;
import org.springframework.beans.factory.annotation.Autowired;

import java.util.Set;

@Route(value = "contracts/:id", layout = MainView.class)
@ViewController(id = "Contract.detail")
@ViewDescriptor(path = "contract-detail-view.xml")
@EditedEntityContainer("contractDc")
public class ContractDetailView extends StandardDetailView<Contract> {

    @Autowired
    private Copier copier;
    @Autowired
    private ContractService contractService;
    @ViewComponent
    private DataContext dataContext;
    @ViewComponent
    private JmixButton approveButton;
    @ViewComponent
    private JmixButton reviseButton;
    @ViewComponent
    private JmixButton rejectButton;
    @Autowired
    private Notifications notifications;

    @Subscribe(id = "approveButton", subject = "clickListener")
    public void onApproveButtonClick(final ClickEvent<JmixButton> event) {
        changeContractStatus(ContractStatus.APPROVED);
    }

    @Subscribe(id = "reviseButton", subject = "clickListener")
    public void onReviseButtonClick(final ClickEvent<JmixButton> event) {
        changeContractStatus(ContractStatus.DRAFT);
    }

    @Subscribe(id = "rejectButton", subject = "clickListener")
    public void onRejectButtonClick(final ClickEvent<JmixButton> event) {
        changeContractStatus(ContractStatus.REJECTED);
    }

    private void changeContractStatus(ContractStatus status) {
        // Make a copy
        Contract contractCopy = copier.copy(getEditedEntity());

        // Pass the copy to the service
        Contract changedContract = contractService.changeStatus(contractCopy, status);

        // Merge the saved entity to DataContext
        var ignored = dataContext.merge(changedContract);

        // Reset the view "modified" state
        clearChanges();

        notifications.create("Status changed").withPosition(Notification.Position.TOP_END).show();
    }

    @Install(target = Target.DATA_CONTEXT)
    private Set<Object> saveDelegate(final SaveContext saveContext) {
        // Make a copy
        Contract contractCopy = copier.copy(getEditedEntity());

        // Pass the copy to the service
        Contract savedContract = contractService.saveContract(contractCopy);

        notifications.create("Changes saved").withPosition(Notification.Position.TOP_END).show();

        // Return the saved entity. It will be merged to DataContext automatically.
        return Set.of(savedContract);
    }

    @Subscribe
    public void onReady(final ReadyEvent event) {
        setShowSaveNotification(false);
        updateButtons(getEditedEntity().getStatus());
    }

    @Subscribe(id = "contractDc", target = Target.DATA_CONTAINER)
    public void onContractDcItemPropertyChange(final InstanceContainer.ItemPropertyChangeEvent<Contract> event) {
        if (event.getProperty().equals("status")) {
            updateButtons((ContractStatus) event.getValue());
        }
    }

    private void updateButtons(ContractStatus status) {
        approveButton.setEnabled(status != ContractStatus.APPROVED);
        reviseButton.setEnabled(status != ContractStatus.DRAFT);
        rejectButton.setEnabled(status != ContractStatus.REJECTED);
    }
}



ContractService.java

package io.jmix.uisamples.view.flowui.cookbook.customservice1;

import io.jmix.core.DataManager;
import io.jmix.uisamples.entity.Contract;
import io.jmix.uisamples.entity.ContractStatus;
import org.apache.commons.lang3.StringUtils;
import org.springframework.stereotype.Component;

import java.time.LocalDateTime;

@Component
public class ContractService {

    private final DataManager dataManager;

    public ContractService(DataManager dataManager) {
        this.dataManager = dataManager;
    }

    public Contract changeStatus(Contract contract, ContractStatus status) {
        contract.setStatus(status);

        String comment = "Changed to " + status + " at " + LocalDateTime.now();
        if (StringUtils.isEmpty(contract.getComments()))
            contract.setComments(comment);
        else
            contract.setComments(contract.getComments() + "\n" + comment);

        Contract savedContract = dataManager.save(contract);

        // Return the saved instance
        return savedContract;
    }

    public Contract saveContract(Contract contract) {
        Contract savedContract = dataManager.save(contract);
        // Return the saved instance
        return savedContract;
    }
}




contract-list-view.xml

<?xml version="1.0" encoding="UTF-8" standalone="no"?>
<view xmlns="http://jmix.io/schema/flowui/view"
      focusComponent="contractsDataGrid">
    <data>
        <collection id="contractsDc"
                    class="io.jmix.uisamples.entity.Contract">
            <fetchPlan extends="_base">
                <property name="customer" fetchPlan="_base"/>
            </fetchPlan>
            <loader id="contractsDl" readOnly="true">
                <query>
                    <![CDATA[select e from Contract e]]>
                </query>
            </loader>
        </collection>
    </data>
    <facets>
        <dataLoadCoordinator auto="true"/>
    </facets>
    <actions>
        <action id="selectAction" type="lookup_select"/>
        <action id="discardAction" type="lookup_discard"/>
    </actions>
    <layout>
        <hbox id="buttonsPanel" classNames="buttons-panel">
            <button id="createButton" action="contractsDataGrid.createAction"/>
            <button id="editButton" action="contractsDataGrid.editAction"/>
        </hbox>
        <dataGrid id="contractsDataGrid"
                  width="100%"
                  minHeight="20em"
                  dataContainer="contractsDc"
                  columnReorderingAllowed="true">
            <actions>
                <action id="createAction" type="list_create" actionVariant="DEFAULT">
                    <properties>
                        <property name="openMode" value="DIALOG"/>
                    </properties>
                </action>
                <action id="editAction" type="list_edit">
                    <properties>
                        <property name="openMode" value="DIALOG"/>
                    </properties>
                </action>
            </actions>
            <columns resizable="true">
                <column property="date"/>
                <column property="number"/>
                <column property="description"/>
                <column property="customer"/>
                <column property="status"/>
                <column property="comments"/>
            </columns>
        </dataGrid>
        <hbox id="lookupActions" visible="false">
            <button id="selectButton" action="selectAction"/>
            <button id="discardButton" action="discardAction"/>
        </hbox>
    </layout>
</view>




ContractListView.java

package io.jmix.uisamples.view.flowui.cookbook.customservice1;

import io.jmix.flowui.model.CollectionLoader;
import io.jmix.flowui.view.*;
import io.jmix.uisamples.entity.Contract;


@ViewController(id = "saving-entity-by-service")
@ViewDescriptor(path = "contract-list-view.xml")
public class ContractListView extends StandardListView<Contract> {

    @ViewComponent
    private CollectionLoader<Contract> contractsDl;

    @Install(to = "contractsDataGrid.createAction", subject = "afterCloseHandler")
    private void contractsDataGridCreateActionAfterCloseHandler(final DialogWindow.AfterCloseEvent<ContractListView> afterCloseEvent) {
        contractsDl.load();
    }

    @Install(to = "contractsDataGrid.editAction", subject = "afterCloseHandler")
    private void contractsDataGridEditActionAfterCloseHandler(final DialogWindow.AfterCloseEvent<ContractListView> afterCloseEvent) {
        contractsDl.load();
    }
}

