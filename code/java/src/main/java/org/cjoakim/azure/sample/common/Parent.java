package org.cjoakim.azure.sample.common;

public class Parent {

    public Parent() {
    }

    public Parent(String firstName) {
        this.firstName = firstName;
    }

    public String getFamilyName() {
        return familyName;
    }

    public void setFamilyName(String familyName) {
        this.familyName = familyName;
    }

    public String getFirstName() {
        return firstName;
    }

    public void setFirstName(String firstName) {
        this.firstName = firstName;
    }

    private String familyName;
    private String firstName;
}
