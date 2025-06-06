CREATE DATABASE OrtoFix;

USE OrtoFix;

CREATE TABLE Aluno (
    idAluno INT PRIMARY KEY AUTO_INCREMENT,
    nomeAluno VARCHAR(100) NOT NULL,
    cpfAluno VARCHAR(11) NOT NULL UNIQUE,
    emailAluno VARCHAR(100) NOT NULL UNIQUE,
    senhaAluno VARCHAR(20) NOT NULL,
    status ENUM('ativo', 'inativo') NOT NULL DEFAULT 'ativo',
);

CREATE TABLE Professor (
    idProfessor INT PRIMARY KEY AUTO_INCREMENT,
    nomeProfessor VARCHAR(100) NOT NULL,
    cpfProfessor VARCHAR(11) NOT NULL UNIQUE,
    emailProfessor VARCHAR(100) NOT NULL UNIQUE,
    senhaProfessor VARCHAR(20) NOT NULL,
    status ENUM('ativo', 'inativo') NOT NULL DEFAULT 'ativo',
);

CREATE TABLE Atividade (
    idProfessor INT NOT NULL,
    idAtividade INT PRIMARY KEY AUTO_INCREMENT,
    nomeAtividade VARCHAR(100) NOT NULL,
    tipoAtividade ENUM('%', '$') NOT NULL,
    diffAtividade INT NOT NULL,
    descricaoAtividade TEXT,
    FOREIGN KEY (idProfessor) REFERENCES Professor(idProfessor)
);

CREATE TABLE AtividadeFeita (
    idAtividadeFeita INT PRIMARY KEY AUTO_INCREMENT,
    idAluno INT NOT NULL,
    idAtividade INT NOT NULL,
    idProfessor INT NOT NULL,
    dataAtividadeFeita DATETIME DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (idAluno) REFERENCES Aluno(idAluno),
    FOREIGN KEY (idAtividade) REFERENCES Atividade(idAtividade),
    FOREIGN KEY (idProfessor) REFERENCES Professor(idProfessor)
);


INSERT INTO Aluno (nomeAluno, cpfAluno, emailAluno, senhaAluno, status)
VALUES
('Pietro Santos', '47808481807', 'pietro.santos.senai@gmail.com', 'senha123', 'ativo');
