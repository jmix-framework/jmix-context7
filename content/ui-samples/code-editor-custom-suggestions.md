<Path>Components > CodeEditor > CodeEditor with custom suggestions</Path>

The `codeEditor` component supports the ability to set your own autocompletions. You can add autocompletion by setting
the `suggester` property in the component. This can be done eather declaratively using the `@Install` annotation or
programmatically using the `CodeEditor#setSuggester(Suggester)` method.

In addition, it is possible to define a regular expression that will open a popup window with autocompletions. Any
entered sequence of characters that satisfies the set regular expression will initiate the opening of popup window. In
this example, in addition to the standard keyboard shortcut, the popup window with autocompletions can be opened after
entering *the dot character* (`.`).


code-editor-custom-suggestions.xml

<view xmlns="http://jmix.io/schema/flowui/view">
    <layout>
        <codeEditor id="codeEditor" height="100%" minHeight="15em"
                    suggestOn="\."/>
    </layout>
</view>




CodeEditorCustomSuggestionsSample.java

package io.jmix.uisamples.view.flowui.components.codeeditor.customsuggestions;

import io.jmix.core.DataManager;
import io.jmix.core.FetchPlan;
import io.jmix.flowui.kit.component.codeeditor.autocomplete.Suggester;
import io.jmix.flowui.kit.component.codeeditor.autocomplete.Suggestion;
import io.jmix.flowui.view.Install;
import io.jmix.flowui.view.StandardView;
import io.jmix.flowui.view.ViewController;
import io.jmix.flowui.view.ViewDescriptor;
import io.jmix.uisamples.entity.Customer;
import org.springframework.beans.factory.annotation.Autowired;

import java.util.List;

@ViewController("code-editor-custom-suggestions")
@ViewDescriptor("code-editor-custom-suggestions.xml")
public class CodeEditorCustomSuggestionsSample extends StandardView {

    @Autowired
    private DataManager dataManager;

    @Install(to = "codeEditor", subject = "suggester")
    public List<Suggestion> codeEditorSuggestions(Suggester.SuggestionContext context) {
        return loadCustomers().stream()
                .map(customer -> new Suggestion(customer.getInstanceName(), customer.getInstanceName(), "Customer"))
                .toList();
    }

    private List<Customer> loadCustomers() {
        return dataManager.load(Customer.class)
                .all()
                .fetchPlan(FetchPlan.INSTANCE_NAME)
                .list();
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
import org.jspecify.annotations.Nullable;

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


