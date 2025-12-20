<Path>Dialogs and notifications > Dialogs > Input dialog</Path>

The Dialogs interface is designed to display standard dialogs windows. Its createInputDialog() method is the entry point to the fluent API that allows you to construct and show input dialogs.

input-dialog.xml

<view xmlns="http://jmix.io/schema/flowui/view">
    <layout classNames="flex-row flex-wrap">
        <button id="standardDialogButton" text="Standard dialog"/>
        <button id="customParameterDialogButton" text="Custom parameter"/>
        <button id="customActionsDialogButton" text="Custom Actions"/>
        <button id="validationDialogButton" text="Validation"/>
    </layout>
</view>




InputDialogSample.java

package io.jmix.uisamples.view.flowui.dialogsandnotifications.dialogs.input;

import com.google.common.base.Strings;
import com.vaadin.flow.component.ClickEvent;
import com.vaadin.flow.component.Html;
import io.jmix.core.DataManager;
import io.jmix.core.MetadataTools;
import io.jmix.flowui.Dialogs;
import io.jmix.flowui.Notifications;
import io.jmix.flowui.UiComponents;
import io.jmix.flowui.action.inputdialog.InputDialogAction;
import io.jmix.flowui.app.inputdialog.DialogActions;
import io.jmix.flowui.app.inputdialog.DialogOutcome;
import io.jmix.flowui.app.inputdialog.InputDialog;
import io.jmix.flowui.app.inputdialog.InputParameter;
import io.jmix.flowui.component.combobox.JmixComboBox;
import io.jmix.flowui.component.validation.ValidationErrors;
import io.jmix.flowui.kit.action.ActionVariant;
import io.jmix.flowui.kit.component.button.JmixButton;
import io.jmix.flowui.view.StandardView;
import io.jmix.flowui.view.Subscribe;
import io.jmix.flowui.view.ViewController;
import io.jmix.flowui.view.ViewDescriptor;
import io.jmix.uisamples.entity.Customer;
import io.jmix.uisamples.entity.CustomerGrade;
import org.springframework.beans.factory.annotation.Autowired;

@ViewController("input-dialog")
@ViewDescriptor("input-dialog.xml")
public class InputDialogSample extends StandardView {

    @Autowired
    protected Dialogs dialogs;
    @Autowired
    protected Notifications notifications;
    @Autowired
    protected MetadataTools metadataTools;
    @Autowired
    protected UiComponents uiComponents;
    @Autowired
    protected DataManager dataManager;

    @Subscribe("standardDialogButton")
    protected void onStandardDialogButtonClick(ClickEvent<JmixButton> event) {
        dialogs.createInputDialog(this)
                .withHeader("Enter values")
                .withLabelsPosition(Dialogs.InputDialogBuilder.LabelsPosition.TOP)
                .withParameters(
                        InputParameter.stringParameter("name")
                                .withLabel("Name")
                                .withRequired(true),
                        InputParameter.doubleParameter("quantity")
                                .withLabel("Quantity")
                                .withDefaultValue(1.0),
                        InputParameter.entityParameter("customer", Customer.class)
                                .withLabel("Customer"),
                        InputParameter.enumParameter("grade", CustomerGrade.class)
                                .withLabel("Grade")
                )
                .withActions(DialogActions.OK_CANCEL)
                .withCloseListener(closeEvent -> {
                    if (!closeEvent.closedWith(DialogOutcome.OK)) {
                        return;
                    }

                    String name = closeEvent.getValue("name");
                    Double quantity = closeEvent.getValue("quantity");
                    Customer customer = closeEvent.getValue("customer");
                    CustomerGrade grade = closeEvent.getValue("grade");

                    String htmlContent = "<h4>Entered Values</h4>" +
                            "<strong>Name:</strong> " + name +
                            "<br/><strong>Quantity:</strong> " + quantity +
                            "<br/><strong>Customer:</strong> " + metadataTools.format(customer) +
                            "<br/><strong>Grade:</strong> " + metadataTools.format(grade);
                    Html notificationContent = new Html("<div>" + htmlContent + "</div>");
                    notifications.show(notificationContent);
                })
                .open();
    }

    @Subscribe("customParameterDialogButton")
    protected void onCustomParameterDialogButtonClick(ClickEvent<JmixButton> event) {
        dialogs.createInputDialog(this)
                .withHeader("Enter values")
                .withLabelsPosition(Dialogs.InputDialogBuilder.LabelsPosition.TOP)
                .withParameters(
                        InputParameter.stringParameter("name")
                                .withLabel("Name"),
                        InputParameter.parameter("customer")
                                .withLabel("Customer")
                                .withField(() -> {
                                    JmixComboBox<Customer> field = uiComponents.create(JmixComboBox.class);
                                    field.setItems(dataManager.load(Customer.class).all().list());
                                    field.setWidthFull();
                                    return field;
                                })
                )
                .withActions(DialogActions.OK_CANCEL)
                .withCloseListener(closeEvent -> {
                    if (!closeEvent.closedWith(DialogOutcome.OK)) {
                        return;
                    }

                    String name = closeEvent.getValue("name");
                    Customer customer = closeEvent.getValue("customer");

                    String htmlContent = "<h4>Entered Values</h4>" +
                            "<strong>Name:</strong> " + name +
                            "<br/><strong>Quantity:</strong> " + metadataTools.format(customer);
                    Html notificationContent = new Html("<div>" + htmlContent + "</div>");
                    notifications.show(notificationContent);
                })
                .open();
    }

    @Subscribe("customActionsDialogButton")
    protected void onCustomActionsDialogButtonClick(ClickEvent<JmixButton> event) {
        dialogs.createInputDialog(this)
                .withHeader("Enter values")
                .withLabelsPosition(Dialogs.InputDialogBuilder.LabelsPosition.TOP)
                .withParameters(
                        InputParameter.stringParameter("name")
                                .withLabel("Name")
                )
                .withActions(
                        InputDialogAction.action("confirm")
                                .withText("Confirm")
                                .withVariant(ActionVariant.PRIMARY)
                                .withHandler(actionEvent -> {
                                    InputDialogAction inputDialogAction = ((InputDialogAction) actionEvent.getSource());
                                    InputDialog inputDialog = inputDialogAction.getInputDialog();

                                    String name = inputDialog.getValue("name");
                                    inputDialog.closeWithDefaultAction();

                                    String htmlContent = "<h4>Entered Values</h4>" +
                                            "<strong>Name:</strong> " + name;
                                    Html notificationContent = new Html("<div>" + htmlContent + "</div>");
                                    notifications.show(notificationContent);
                                }),
                        InputDialogAction.action("refuse")
                                .withText("Refuse")
                                .withValidationRequired(false)
                                .withHandler(actionEvent -> {
                                    InputDialogAction inputDialogAction = ((InputDialogAction) actionEvent.getSource());
                                    InputDialog inputDialog = inputDialogAction.getInputDialog();
                                    inputDialog.closeWithDefaultAction();
                                })
                )
                .open();
    }

    @Subscribe("validationDialogButton")
    protected void onValidationDialogButtonClick(ClickEvent<JmixButton> event) {
        dialogs.createInputDialog(this)
                .withHeader("Enter values")
                .withLabelsPosition(Dialogs.InputDialogBuilder.LabelsPosition.TOP)
                .withParameters(
                        InputParameter.stringParameter("name")
                                .withLabel("Name"),
                        InputParameter.entityParameter("customer", Customer.class)
                                .withLabel("Customer")
                )
                .withValidator(context -> {
                    String name = context.getValue("name");
                    Customer customer = context.getValue("customer");
                    if (Strings.isNullOrEmpty(name) && customer == null) {
                        return ValidationErrors.of("Enter name or select a customer");
                    }
                    return ValidationErrors.none();
                })
                .withActions(DialogActions.OK_CANCEL)
                .withCloseListener(closeEvent -> {
                    if (!closeEvent.closedWith(DialogOutcome.OK)) {
                        return;
                    }

                    String name = closeEvent.getValue("name");
                    Customer customer = closeEvent.getValue("customer");

                    String htmlContent = "<h4>Entered Values</h4>" +
                            "<strong>Name:</strong> " + name +
                            "<br/><strong>Customer:</strong> " + metadataTools.format(customer);
                    Html notificationContent = new Html("<div>" + htmlContent + "</div>");
                    notifications.show(notificationContent);
                })
                .open();
    }
}




Customer.java

package io.jmix.uisamples.entity;

import io.jmix.core.entity.annotation.JmixGeneratedValue;
import io.jmix.core.metamodel.annotation.DependsOnProperties;
import io.jmix.core.metamodel.annotation.InstanceName;
import io.jmix.core.metamodel.annotation.JmixEntity;
import jakarta.persistence.Column;
import jakarta.persistence.Entity;
import jakarta.persistence.Id;
import jakarta.persistence.Table;
import jakarta.validation.constraints.Email;
import org.springframework.lang.Nullable;

import java.util.UUID;

@Table(name = "CUSTOMER")
@Entity
@JmixEntity
public class Customer {

    @Id
    @Column(name = "ID", nullable = false)
    @JmixGeneratedValue
    protected UUID id;

    @Column(name = "NAME", length = 50, nullable = false)
    protected String name;

    @Column(name = "LAST_NAME", length = 100, nullable = false)
    protected String lastName;

    @Email
    @Column(name = "EMAIL", nullable = false)
    protected String email;

    @Column(name = "AGE")
    protected Integer age;

    @Column(name = "ACTIVE", nullable = false)
    protected Boolean active = false;

    @Column(name = "GRADE")
    protected Integer grade;

    public Boolean getActive() {
        return active;
    }

    public Customer() {
        this.id = UUID.randomUUID();
    }

    @InstanceName
    @DependsOnProperties({"name", "lastName"})
    public String getInstanceName() {
        return name + " " + lastName;
    }

    public UUID getId() {
        return id;
    }

    public void setId(UUID id) {
        this.id = id;
    }

    public void setGrade(@Nullable CustomerGrade grade) {
        this.grade = grade == null ? null : grade.getId();
    }

    @Nullable
    public CustomerGrade getGrade() {
        return grade == null ? null : CustomerGrade.fromId(grade);
    }

    public void setActive(Boolean active) {
        this.active = active;
    }

    public Boolean isActive() {
        return active;
    }

    public void setName(String name) {
        this.name = name;
    }

    public String getName() {
        return name;
    }

    public void setLastName(String lastName) {
        this.lastName = lastName;
    }

    public String getLastName() {
        return lastName;
    }

    public String getEmail() {
        return email;
    }

    public void setEmail(String email) {
        this.email = email;
    }

    public void setAge(Integer age) {
        this.age = age;
    }

    public Integer getAge() {
        return age;
    }
}




CustomerGrade.java

package io.jmix.uisamples.entity;

import io.jmix.core.metamodel.datatype.EnumClass;
import org.springframework.lang.Nullable;

public enum CustomerGrade implements EnumClass<Integer> {

    PREMIUM(10),
    HIGH(20),
    STANDARD(30);

    private final Integer id;

    CustomerGrade(Integer id) {
        this.id = id;
    }

    @Override
    public Integer getId() {
        return id;
    }

    @Nullable
    public static CustomerGrade fromId(Integer id) {
        for (CustomerGrade grade : CustomerGrade.values()) {
            if (grade.getId().equals(id))
                return grade;
        }
        return null;
    }
}


